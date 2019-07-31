from QueriesFactory import QuestionnaireQueryKeys, AssessmentQueryKeys, WatchDataQueryKeys, ActionTypes
from QuestionnaireReportResults import QuestionnaireReportResults, AssessmentReportResults, AssessmentDataValidation


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
                                                          None,  # Start time - not needed for schedule comparison
                                                          None,  # End_time - not needed for schedule comparison
                                                          None,  # Status - not needed for schedule comparision
                                                          json_file[QuestionnaireQueryKeys.HOUR.value],
                                                          json_file[QuestionnaireQueryKeys.MINUTE.value])
        return questionnaire_object

    if action == ActionTypes.ASSESSMENT_REPORT.name or action == ActionTypes.GYRO_DATA.name:
        # create an object from the athena scan
        assessment_object = AssessmentReportResults(json_file[AssessmentQueryKeys.USER_NAME.value],
                                                    json_file[AssessmentQueryKeys.ASSESSMENT_NAME.value],
                                                    None,  # Action - not needed for comparing
                                                    json_file[AssessmentQueryKeys.ASSESSMENT_START_TIME.value],
                                                    json_file[AssessmentQueryKeys.ASSESSMENT_END_TIME.value],
                                                    None,  # triggered time stamp - not needed for now
                                                    None,  # triggered end time stamp - not needed for now
                                                    json_file[AssessmentQueryKeys.STATUS.value])
        return assessment_object


def parse_athena_results(results, action):
    if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
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
        questionnaire_object = QuestionnaireReportResults(results[QuestionnaireQueryKeys.USER_NAME.value][0],
                                                          results[QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value][0],
                                                          None,  # Action - not needed for comparing
                                                          None,  # Start time - not needed for schedule comparison
                                                          None,  # End_time - not needed for schedule comparison
                                                          None,  # Status - not needed for schedule comparison
                                                          results[QuestionnaireQueryKeys.HOUR.value][0],
                                                          results[QuestionnaireQueryKeys.MINUTE.value][0])
        return questionnaire_object

    if action == ActionTypes.ASSESSMENT_REPORT.name:
        assessment_object = AssessmentReportResults(results[AssessmentQueryKeys.USER_NAME.value][0],
                                                    results[AssessmentQueryKeys.ASSESSMENT_NAME.value][0],
                                                    None,  # Action - not needed for comparing
                                                    results[AssessmentQueryKeys.ASSESSMENT_START_TIME.value][0],
                                                    results[AssessmentQueryKeys.ASSESSMENT_END_TIME.value][0],
                                                    None,  # triggered time stamp - not needed for now
                                                    None,  # triggered end time stamp - not needed for now
                                                    results[AssessmentQueryKeys.STATUS.value][0])
        return assessment_object

    if action == ActionTypes.GYRO_DATA.name:
        gyro_object = AssessmentDataValidation(results[WatchDataQueryKeys.USER_NAME.value][0],
                                               results[WatchDataQueryKeys.ASSESSMENT_ID.value][0],
                                               results[WatchDataQueryKeys.ACTUAL.value][0],
                                               results[WatchDataQueryKeys.EXPECTED.value][0])
        return gyro_object
