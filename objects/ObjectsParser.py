from objects.Objects import QuestionnaireReportResults, AssessmentReportResults, AssessmentDataValidation, \
    DiaryReportResults, MedicationReportResults
from queries.AssessmentQueriesFactory import AssessmentQueryKeys
from queries.DiaryQueriesFactory import DiaryQueryKeys
from queries.QueriesManager import ActionTypes
from queries.QuestionnaireQueriesFactory import QuestionnaireQueryKeys
from queries.WatchDataQueryFactory import WatchDataQueryKeys
from queries.MedicationQueriesFactory import MedicationQueryKeys


def parse_json_file(json_file, action):
    try:
        if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
            # create an object from the athena scan
            questionnaire_object = QuestionnaireReportResults(json_file[QuestionnaireQueryKeys.USER_NAME.value],
                                                              json_file[
                                                                  QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value],
                                                              None,  # Action
                                                              json_file[
                                                                  QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_START.value],
                                                              json_file[
                                                                  QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_END.value],
                                                              json_file[QuestionnaireQueryKeys.STATUS.value],
                                                              None,  # Hour
                                                              None)  # Minute
            answers = json_file[QuestionnaireQueryKeys.ANSWER.value]

            for index in range(0, len(answers)):
                questionnaire_object.answers.append(answers[str(index)])

            return questionnaire_object

        if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
            # create an object from the athena scan
            questionnaire_object = QuestionnaireReportResults(json_file[QuestionnaireQueryKeys.USER_NAME.value],
                                                              json_file[
                                                                  QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value],
                                                              None,  # Action
                                                              None,  # Start time
                                                              None,  # End_time
                                                              None,  # Status
                                                              json_file[QuestionnaireQueryKeys.HOUR.value],
                                                              json_file[QuestionnaireQueryKeys.MINUTE.value])
            return questionnaire_object

        if action == ActionTypes.ASSESSMENT_REPORT.name or action == ActionTypes.GYRO_DATA.name:
            # create an object from the athena scan
            assessment_object = AssessmentReportResults(json_file[AssessmentQueryKeys.USER_NAME.value],
                                                        json_file[AssessmentQueryKeys.ASSESSMENT_NAME.value],
                                                        None,  # Action
                                                        json_file[AssessmentQueryKeys.ASSESSMENT_START_TIME.value],
                                                        json_file[AssessmentQueryKeys.ASSESSMENT_END_TIME.value],
                                                        None,  # Triggered_STS
                                                        None,  # Triggered_ETS
                                                        json_file[AssessmentQueryKeys.STATUS.value],
                                                        None, # Triggered name
                                                        json_file[AssessmentQueryKeys.NUMBER_OF_STEPS.value])
            return assessment_object

        if action == ActionTypes.DIARY_REPORT.name:
            diary_object = DiaryReportResults(json_file[DiaryQueryKeys.USER_NAME.value],
                                              json_file[DiaryQueryKeys.DIARY_ID.value],
                                              None,
                                              json_file[DiaryQueryKeys.DIARY_TIMESTAMP_START.value],
                                              json_file[DiaryQueryKeys.DIARY_TIMESTAMP_END.value],
                                              json_file[DiaryQueryKeys.STATUS.value])

            answers = json_file[DiaryQueryKeys.ANSWER.value]

            for index in range(0, len(answers)):
                diary_object.answers.append(answers[str(index)])

            return diary_object

        if action == ActionTypes.MEDICATION_SCHEDULE.name:
            medication_object = MedicationReportResults(json_file[MedicationQueryKeys.USER_NAME.value],
                                                        json_file[MedicationQueryKeys.MEDICATION_NAME.value],
                                                        None,
                                                        json_file[MedicationQueryKeys.EFFECTIVE_START.value],
                                                        json_file[MedicationQueryKeys.EFFECTIVE_END.value],
                                                        None,
                                                        None,
                                                        None,
                                                        json_file[MedicationQueryKeys.HOUR.value],
                                                        json_file[MedicationQueryKeys.MINUTE.value])
            return medication_object

        if action == ActionTypes.MEDICATION_REPORT.name:
            medication_object = MedicationReportResults(json_file[MedicationQueryKeys.USER_NAME.value],
                                                        json_file[MedicationQueryKeys.MEDICATION_NAME.value],
                                                        None,
                                                        None,
                                                        None,
                                                        json_file[MedicationQueryKeys.STATUS.value],
                                                        json_file[MedicationQueryKeys.MEDICATION_TAKEN_TS.value],
                                                        json_file[MedicationQueryKeys.REPORT_TS.value],
                                                        None,
                                                        None)
            return medication_object

        if action == ActionTypes.MEDICATION_SKIPPED.name:
            medication_object = MedicationReportResults(json_file[MedicationQueryKeys.USER_NAME.value],
                                                        json_file[MedicationQueryKeys.MEDICATION_NAME.value],
                                                        None,
                                                        None,
                                                        None,
                                                        json_file[MedicationQueryKeys.STATUS.value],
                                                        None,
                                                        json_file[MedicationQueryKeys.REPORT_TS.value],
                                                        None,
                                                        None)
            return medication_object

        if action == ActionTypes.TRIGGERED_QUESTIONNAIRE.name:
            # create an object from the athena scan
            assessment_object = AssessmentReportResults(json_file[AssessmentQueryKeys.USER_NAME.value],
                                                        None,
                                                        None,  # Action
                                                        None,
                                                        None,
                                                        json_file[AssessmentQueryKeys.TRIGGERED_START_TIME.value],  # Triggered_STS
                                                        json_file[AssessmentQueryKeys.TRIGGERED_END_TIME.value],  # Triggered_ETS
                                                        None,
                                                        json_file[AssessmentQueryKeys.TRIGGERED_QUESTIONNAIRE.value], # Triggered name
                                                        None)
            return assessment_object

    except KeyError or ValueError:
        return


def parse_athena_results(results, action):
    try:
        if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
            questionnaire_object = QuestionnaireReportResults(results[QuestionnaireQueryKeys.USER_NAME.value][0],
                                                              results[QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value][
                                                                  0],
                                                              None,  # Action
                                                              results[
                                                                  QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_START.value][
                                                                  0],
                                                              results[
                                                                  QuestionnaireQueryKeys.QUESTIONNAIRE_TIMESTAMP_END.value][
                                                                  0],
                                                              results[QuestionnaireQueryKeys.STATUS.value][0],
                                                              None,
                                                              # Hour
                                                              None)  # Minute
            answers = results[QuestionnaireQueryKeys.ANSWER.value]

            for index in range(0, answers.size):
                questionnaire_object.answers.append(answers[index])

            return questionnaire_object

        if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
            questionnaire_object = QuestionnaireReportResults(results[QuestionnaireQueryKeys.USER_NAME.value][0],
                                                              results[QuestionnaireQueryKeys.QUESTIONNAIRE_NAME.value][
                                                                  0],
                                                              None,  # Action
                                                              None,  # Start time
                                                              None,  # End_time
                                                              None,  # Status
                                                              results[QuestionnaireQueryKeys.HOUR.value][0],
                                                              results[QuestionnaireQueryKeys.MINUTE.value][0])
            return questionnaire_object

        if action == ActionTypes.ASSESSMENT_REPORT.name:
            assessment_object = AssessmentReportResults(results[AssessmentQueryKeys.USER_NAME.value][0],
                                                        results[AssessmentQueryKeys.ASSESSMENT_NAME.value][0],
                                                        None,  # Action
                                                        results[AssessmentQueryKeys.ASSESSMENT_START_TIME.value][0],
                                                        results[AssessmentQueryKeys.ASSESSMENT_END_TIME.value][0],
                                                        None,  # Triggered_STS
                                                        None,  # Triggered_ETS
                                                        results[AssessmentQueryKeys.STATUS.value][0])

            number_of_steps = results[QuestionnaireQueryKeys.USER_NAME.value]
            assessment_object.numeber_of_steps = number_of_steps.size

            return assessment_object

        if action == ActionTypes.GYRO_DATA.name:
            gyro_object = AssessmentDataValidation(results[WatchDataQueryKeys.USER_NAME.value][0],
                                                   results[WatchDataQueryKeys.ASSESSMENT_ID.value][0],
                                                   results[WatchDataQueryKeys.ACTUAL.value][0],
                                                   results[WatchDataQueryKeys.EXPECTED.value][0])
            return gyro_object

        if action == ActionTypes.DIARY_REPORT.name:
            diary_object = DiaryReportResults(results[DiaryQueryKeys.USER_NAME.value][0],
                                              results[DiaryQueryKeys.DIARY_ID.value][0],
                                              None,
                                              results[DiaryQueryKeys.DIARY_TIMESTAMP_START.value][0],
                                              results[DiaryQueryKeys.DIARY_TIMESTAMP_END.value][0],
                                              results[DiaryQueryKeys.STATUS.value][0])

            answers = results[DiaryQueryKeys.ANSWER.value]

            for index in range(0, len(answers)):
                diary_object.answers.append(answers[index])

            return diary_object

        if action == ActionTypes.MEDICATION_SCHEDULE.name:
            medication_object = MedicationReportResults(results[MedicationQueryKeys.USER_NAME.value][0],
                                                        results[MedicationQueryKeys.MEDICATION_NAME.value][0],
                                                        None,
                                                        results[MedicationQueryKeys.EFFECTIVE_START.value][0],
                                                        results[MedicationQueryKeys.EFFECTIVE_END.value][0],
                                                        None,
                                                        None,
                                                        None,
                                                        results[MedicationQueryKeys.HOUR.value][0],
                                                        results[MedicationQueryKeys.MINUTE.value][0])

            if len(medication_object.hour) == 1:
                medication_object.hour = "0" + medication_object.hour
            if len(medication_object.minute) == 1:
                medication_object.minute = "0" + medication_object.minute

            return medication_object

        if action == ActionTypes.MEDICATION_REPORT.name:
            medication_object = MedicationReportResults(results[MedicationQueryKeys.USER_NAME.value][0],
                                                        results[MedicationQueryKeys.MEDICATION_NAME.value][0],
                                                        None,
                                                        None,
                                                        None,
                                                        results[MedicationQueryKeys.STATUS.value][0],
                                                        results[MedicationQueryKeys.MEDICATION_TAKEN_TS.value][0],
                                                        results[MedicationQueryKeys.REPORT_TS.value][0],
                                                        None,
                                                        None)
            return medication_object

        if action == ActionTypes.MEDICATION_SKIPPED.name:
            medication_object = MedicationReportResults(results[MedicationQueryKeys.USER_NAME.value][0],
                                                        results[MedicationQueryKeys.MEDICATION_NAME.value][0],
                                                        None,
                                                        None,
                                                        None,
                                                        results[MedicationQueryKeys.STATUS.value][0],
                                                        None,
                                                        results[MedicationQueryKeys.REPORT_TS.value][0],
                                                        None,
                                                        None)
            return medication_object

        if action == ActionTypes.TRIGGERED_QUESTIONNAIRE.name:
            assessment_object = AssessmentReportResults(results[AssessmentQueryKeys.USER_NAME.value][0],
                                                        None,
                                                        None,
                                                        None,
                                                        None,
                                                        results[AssessmentQueryKeys.TRIGGERED_QUESTIONNAIRE_START.value][0],
                                                        results[AssessmentQueryKeys.TRIGGERED_QUESTIONNAIRE_END.value][0],
                                                        None,
                                                        results[AssessmentQueryKeys.TRIGGERED_QUESTIONNAIRE_NAME.value][0],
                                                        None)
            return assessment_object

    except KeyError or ValueError:
        return
