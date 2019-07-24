from QueriesFactory import basicQuestionnaireReportSqlQuery, basicQuestionnaireScheduleQuery, QuestionnaireQueryKeys, \
    ActionTypes
from QuestionnaireReportResults import QuestionnaireReportResults
from pyathenajdbc import connect
import pandas as pd
import json

logs = []
tests_failed = 0


def add_log(log):
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


def parse_json_file(json_file, action):
    if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
        # create an object from the athena scan
        questionnaire_object = QuestionnaireReportResults(json_file[QuestionnaireQueryKeys.USER_NAME.value],
                                                          json_file[QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value],
                                                          None,  # Action - not needed for comparing
                                                          json_file[
                                                              QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_START.value],
                                                          json_file[
                                                              QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_END.value],
                                                          json_file[QuestionnaireQueryKeys.STATUS.value],
                                                          None,  # Hour not needed for questionnaire report comparison
                                                          None)  # Minute not needed for questionnaire report comparison
        answers = json_file[QuestionnaireQueryKeys.ANSWER.value]

        for index in range(0, len(answers)):
            questionnaire_object.questions_answers.append(answers[str(index)])

        return questionnaire_object

    if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
        # create an object from the athena scan
        questionnaire_object = QuestionnaireReportResults(json_file[QuestionnaireQueryKeys.USER_NAME.value],
                                                          json_file[QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value],
                                                          None,  # Action - not needed for comparing
                                                          None,  # Start time - not needed for shcedile comaprison
                                                          None,  # End_time - not needed for shcedile comaprison
                                                          None,  # Status - not needed for schedule comparision
                                                          json_file[QuestionnaireQueryKeys.HOUR.value],
                                                          json_file[QuestionnaireQueryKeys.MINUTE.value])
        return questionnaire_object


def parse_athena_results(results, action):
    if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
        # create an object from the athena scan
        questionnaire_object = QuestionnaireReportResults(results[QuestionnaireQueryKeys.USER_NAME.value][0],
                                                          results[QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value][0],
                                                          None,  # Action - not needed for comparing
                                                          results[
                                                              QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_START.value][
                                                              0],
                                                          results[
                                                              QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_END.value][
                                                              0],
                                                          results[QuestionnaireQueryKeys.STATUS.value][0],
                                                          None,  # Hour not needed for questionnaire report comparison
                                                          None)  # Minute not needed for questionnaire report comparison
        answers = results[QuestionnaireQueryKeys.ANSWER.value]

        for index in range(0, answers.size):
            questionnaire_object.questions_answers.append(answers[index])

        return questionnaire_object

    if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
        # create an object from the athena scan
        questionnaire_object = QuestionnaireReportResults(results[QuestionnaireQueryKeys.USER_NAME.value][0],
                                                          results[QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value][0],
                                                          None,  # Action - not needed for comparing
                                                          None,  # Start time - not needed for shcedile comaprison
                                                          None,  # End_time - not needed for shcedile comaprison
                                                          None,  # Status - not needed for schedule comparision
                                                          results[QuestionnaireQueryKeys.HOUR.value][0],
                                                          results[QuestionnaireQueryKeys.MINUTE.value][0])
        return questionnaire_object


def create_query(object, action):
    if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
        return basicQuestionnaireReportSqlQuery.substitute(user_name=object.user_name,
                                                           questionnaire_name=object.questionnaire_name,
                                                           questionnaire_timestamp_start=object.questionnaire_timestamp_start,
                                                           questionnaire_timestamp_end=object.questionnaire_timestamp_end)
    if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
        return basicQuestionnaireScheduleQuery.substitute(user_name=object.user_name,
                                                          questionnaire_name=object.questionnaire_name,
                                                          )


def scan_athena(query):
    try:
        conn = connect(profile_name='health-customers',
                       s3_staging_dir='s3://aws-athena-query-results-eu-west-1-036573440528/',
                       region_name='eu-west-1',
                       schema_name='kclprep')
        return pd.read_sql(query, conn)
    except ValueError:
        print("Got error")
    finally:
        print("")


def get_files_by_date(daysBack):
    files_to_validate = ['BDD_Test01_QuestionnaireReport']
    return files_to_validate


def main():
    raw_files = get_files_by_date(1)
    for file in raw_files:
        with open(file) as json_file:
            loaded_json = json.load(json_file)
            actions = extract_required_actions(loaded_json)

            for action in actions:
                json_file_object = parse_json_file(loaded_json, action)
                query = create_query(json_file_object, action)
                results = scan_athena(query)
                if results.empty:
                    add_log(json_file.name + " couldn't query from athena, moving to next file...")
                    continue
                athena_results_object = parse_athena_results(results, action)

                if compare_objects_with_action(action, json_file_object, athena_results_object):
                    add_log(json_file.name + "Passed successfully")
                else:
                    add_log(json_file.name + " Failed")
                    add_log(json_file.name + " Expected: " + str(json_file_object))
                    add_log(json_file.name + " Actual " + str(athena_results_object))
    logs.append(str(tests_failed) + "/" + str(len(raw_files)) + " has failed")
    print("\n".join(logs))
    pass


if __name__ == '__main__':
    main()
