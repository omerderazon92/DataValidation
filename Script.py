from datetime import date

import pandas as pd
import requests
from pyathenajdbc import connect
import re

from ObjectsParser import parse_json_file, parse_athena_results
from QueriesFactory import QuestionnaireQueryKeys, ActionTypes, create_query, articfactory_adress

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
    try:
        return loaded_json[QuestionnaireQueryKeys.ACTIONS.value]
    except KeyError or ValueError:
        return


def compare_objects_with_action(action, json_file_object, athena_results_object):
    if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
        if len(json_file_object.questions_answers) != len(athena_results_object.questions_answers):
            return False
        else:
            for index in range(0, len(athena_results_object.questions_answers)):
                if athena_results_object.questions_answers[index] != json_file_object.questions_answers[index]:
                    return False
            if json_file_object.status != athena_results_object.status:
                return False
        return True
    if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
        if json_file_object.hour != athena_results_object.hour or json_file_object.minute != athena_results_object.minute:
            return False
        return True
    if action == ActionTypes.ASSESSMENT_REPORT.name:
        if json_file_object.assessment_name != athena_results_object.assessment_name or json_file_object.status != athena_results_object.status:
            return False
        return True
    if action == ActionTypes.GYRO_DATA.name:
        if athena_results_object.actual / athena_results_object.expected < 0.95:
            return False
        return True
    pass


def scan_athena(query):
    conn = connect(profile_name='health-customers',
                   s3_staging_dir='s3://aws-athena-query-results-eu-west-1-036573440528/',
                   region_name='eu-west-1',
                   schema_name='kclprep')
    return pd.read_sql(query, conn)


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
        return


def main():
    raw_files = get_list_of_files()
    if raw_files:
        for file_name in raw_files:
            # Download the file from the artifactory
            loaded_json = download_file(file_name)
            if loaded_json is None:
                add_log(
                    file_name + " Couldn't parse  into a JSON file, might be empty json. moving to the next file...")
                increment()
                continue

            # Extract the right action from the JSON file
            actions = extract_required_actions(loaded_json)
            if actions is None or len(actions) <= 0:
                add_log(file_name + " Didn't get any action to check - actions list might be empty or nil")
                increment()
                continue

            # Iterates over the actions and validate the right modules
            for action in actions:
                # Parse the JSON file into an object
                json_file_object = parse_json_file(loaded_json, action)
                if json_file_object is None:
                    add_log(file_name + " Couldn't parse the JSON into an object - moving to the next file...")
                    increment()
                    continue

                # Extract an Athena query from the object
                query = create_query(json_file_object, action)
                if query is None:
                    add_log(file_name + " Couldn't extract any query - moving to the next action or file")
                    increment()
                    continue

                # Scan Athena using a connector and the extracted query
                results = scan_athena(query)
                if results.empty:
                    add_log(file_name + " Couldn't query from athena or got an empty results, moving to next "
                                        "action or file...")
                    increment()
                    continue

                # Parse the results into an object
                athena_results_object = parse_athena_results(results, action)
                if athena_results_object is None:
                    add_log(file_name + " Couldn't parse athena DB results into an object, moving to the next action "
                                        "or file...")
                    increment()
                    continue

                # Compare the JSON and Athena results
                if compare_objects_with_action(action, json_file_object, athena_results_object):
                    add_log(file_name + " With " + action + " checking Has Passed successfully")
                else:
                    add_log(file_name + " With " + action + " Has Failed")
                    add_log(file_name + " Expected: " + str(json_file_object))
                    add_log(file_name + " Actual    " + str(athena_results_object))
                    increment()

        logs.append(str(tests_failed) + "/" + str(len(raw_files)) + " Has failed")

    else:
        add_log("Couldn't get any relevant JSON files to validate - aborting process")

    print("\n".join(logs))
    pass


if __name__ == '__main__':
    main()
