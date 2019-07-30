from QueriesFactory import QuestionnaireQueryKeys, ActionTypes, create_query, articfactory_adress
from ObjectsParser import parse_json_file, parse_athena_results
from pyathenajdbc import connect
import pandas as pd
import re
import requests
from datetime import date

logs = []
tests_failed = 0
date = date.today()


def add_log(log):
    global logs
    logs.append(log)


def increment():
    global tests_failed
    tests_failed += 1


def extract_required_actions(loaded_json):
    return loaded_json[QuestionnaireQueryKeys.ACTIONS.value]


def compare_objects_with_action(action, json_file_object, athena_results_object):
    if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
        if len(json_file_object.questions_answers) != len(athena_results_object.questions_answers):
            return False
        else:
            for index in range(0, len(athena_results_object.questions_answers)):
                if athena_results_object.questions_answers[index] != json_file_object.questions_answers[index]:
                    increment()
                    return False
            if json_file_object.status != athena_results_object.status:
                increment()
                return False
        return True
    if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
        if json_file_object.hour != athena_results_object.hour or json_file_object.minute != athena_results_object.minute:
            increment()
            return False
        return True
    pass

def scan_athena(query):
    try:
        conn = connect(profile_name='health-customers',
                       s3_staging_dir='s3://aws-athena-query-results-eu-west-1-036573440528/',
                       region_name='eu-west-1',
                       schema_name='kclprep')
        return pd.read_sql(query, conn)
    finally:
        print("")


def get_list_of_files():
    files = []
    response = requests.get(articfactory_adress, auth=('jenkins', 'jenkins123!'))
    if response:
        response_content = str(response.content)
        if response_content:
            for match in re.finditer('href="BDD(.+?)json', response_content):
                files.append(match.group(0).replace("href=\"", ''))
            return files


def download_file(file_name):
    try:
        response = requests.get(
            articfactory_adress + file_name,
            auth=('jenkins', 'jenkins123!'))
        if response:
            if response.json():
                return response.json()
    except ValueError:
        add_log("Couldn't parse " + file_name + " into a JSON file, might be empty json. moving to the next file...")


def main():
    raw_files = get_list_of_files()
    for file_name in raw_files:
        loaded_json = download_file(file_name)
        if loaded_json is None:
            increment()
            continue
        actions = extract_required_actions(loaded_json)
        if len(actions) <= 0 or actions is None:
            add_log(file_name + " didn't get any action to check, moving to next file...")
            continue

        for action in actions:
            json_file_object = parse_json_file(loaded_json, action)
            query = create_query(json_file_object, action)
            results = scan_athena(query)
            if results.empty:
                add_log(file_name + " couldn't query from athena or got an empty results, moving to next "
                                    "file...")
                increment()
                continue
            athena_results_object = parse_athena_results(results, action)

            if compare_objects_with_action(action, json_file_object, athena_results_object):
                add_log(file_name + " Passed successfully")
            else:
                add_log(file_name + " Failed")
                add_log(file_name + " Expected: " + str(json_file_object))
                add_log(file_name + " Actual    " + str(athena_results_object))

    logs.append(str(tests_failed) + "/" + str(len(raw_files)) + " has failed")
    print("\n".join(logs))
    pass


if __name__ == '__main__':
    main()
