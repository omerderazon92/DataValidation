from QueriesFactory import basicQuestionnaireReportSqlQuery, QuestionnaireQueryKeys
from QuestionnaireReportResults import QuestionnaireReportResults
from pyathenajdbc import connect
import pandas as pd
import json


def main():
    raw_files = get_files_by_date(1)
    for file in raw_files:
        with open(file) as json_file:
            questionnaire_object = parse_json_into_object(json.load(json_file))
            query = create_query_from_object(questionnaire_object)
            results = scan_athena_using(query)
            results_object = parse_results_into_object(results)

            if questionnaire_object == results_object:
                print(json_file.name + " Passed successfully")
            else:
                print(json_file.name + " Failed")
                print("Expected: " + str(questionnaire_object))
                print("Actual" + str(results_object))
    pass


def parse_json_into_object(json_file):
    questionnaire_object = None
    # create an object from the athena scan
    questionnaire_object = QuestionnaireReportResults(json_file[QuestionnaireQueryKeys.USER_NAME.value],
                                                      json_file[QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value],
                                                      json_file[QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_START.value],
                                                      json_file[QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_END.value],
                                                      json_file[QuestionnaireQueryKeys.STATUS.value])
    answers = json_file[QuestionnaireQueryKeys.ANSWER.value]

    for index in range(0, len(answers)):
        questionnaire_object.questions_answers.append(answers[str(index)])

    return questionnaire_object


def parse_results_into_object(results):
    # create an object from the athena scan
    questionnaire_object = QuestionnaireReportResults(results[QuestionnaireQueryKeys.USER_NAME.value][0],
                                                      results[QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value][0],
                                                      results[QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_START.value][0],
                                                      results[QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_END.value][0],
                                                      results[QuestionnaireQueryKeys.STATUS.value][0])
    answers = results[QuestionnaireQueryKeys.ANSWER.value]
    for index in range(0, answers.size):
        questionnaire_object.questions_answers.append(answers[index])

    return questionnaire_object


def scan_athena_using(query):
    try:
        conn = connect(profile_name='health-customers',
                       s3_staging_dir='s3://aws-athena-query-results-eu-west-1-036573440528/',
                       region_name='eu-west-1',
                       schema_name='kclprep')
        return pd.read_sql(query, conn)
    finally:
        print("")


def create_query_from_object(object):
    return basicQuestionnaireReportSqlQuery.substitute(user_name=object.user_name,
                                                       questionnaire_name=object.questionnaire_name,
                                                       questionnaire_timestamp_start=object.questionnaire_timestamp_start,
                                                       questionnaire_timestamp_end=object.questionnaire_timestamp_end)


def get_files_by_date(daysBack):
    files_to_validate = ['BDD_QuestionnaireReport']
    return files_to_validate


if __name__ == '__main__':
    main()
