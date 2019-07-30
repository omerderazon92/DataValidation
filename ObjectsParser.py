from QueriesFactory import QuestionnaireQueryKeys, ActionTypes
from QuestionnaireReportResults import QuestionnaireReportResults


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
                                                          None,  # Start time - not needed for schedule comparison
                                                          None,  # End_time - not needed for schedule comparison
                                                          None,  # Status - not needed for schedule comparison
                                                          results[QuestionnaireQueryKeys.HOUR.value][0],
                                                          results[QuestionnaireQueryKeys.MINUTE.value][0])
        return questionnaire_object
