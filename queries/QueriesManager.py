from enum import Enum

from queries.AssessmentQueriesFactory import basicAssessmentReportQuery, basicTappingReportQuery
from queries.QuestionnaireQueriesFactory import basicQuestionnaireReportSqlQuery, basicQuestionnaireScheduleQuery, \
    QuestionnaireQueryKeys
from queries.DiaryQueriesFactory import basicDiaryReportQuery
from queries.WatchDataQueryFactory import basicGyroQuery
from queries.MedicationQueriesFactory import basicMedicationScheduleQuery, basicMedicationRerportQuery


class ActionTypes(Enum):
    QUESTIONNAIRE_REPORT = "0"
    QUESTIONNAIRE_SCHEDULE = "1"
    ASSESSMENT_REPORT = "2"
    GYRO_DATA = "3"
    DIARY_REPORT = "4"
    MEDICATION_SCHEDULE = "5"
    MEDICATION_REPORT = "6"
    NO_ACTION = "7"
    TAPPING_STEP = "8"
    MEDICATION_SKIPPED = "9"
    TRIGGERED_QUESTIONNAIRE = "10"
    ASSESSMENT_REPORT_RETRY = "12"


def extract_required_actions(loaded_json):
    try:
        return loaded_json[QuestionnaireQueryKeys.ACTIONS.value]
    except KeyError or ValueError:
        return


def create_query(object, action, env):
    try:
        if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
            return basicQuestionnaireReportSqlQuery.substitute(user_name=object.user_name,
                                                               questionnaire_name=object.questionnaire_name,
                                                               questionnaire_timestamp_start=object.questionnaire_timestamp_start,
                                                               questionnaire_timestamp_end=object.questionnaire_timestamp_end,
                                                               env=env)
        if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
            return basicQuestionnaireScheduleQuery.substitute(user_name=object.user_name,
                                                              questionnaire_name=object.questionnaire_name,
                                                              env=env)
        if action == ActionTypes.ASSESSMENT_REPORT.name:
            return basicAssessmentReportQuery.substitute(user_name=object.user_name,
                                                         assessment_name=object.assessment_name,
                                                         assessment_start=object.assessment_start,
                                                         assessment_end=object.assessment_end,
                                                         env=env)

        if action == ActionTypes.GYRO_DATA.name:
            return basicGyroQuery.substitute(user_name=object.user_name,
                                             assessment_end=object.assessment_end,
                                             env=env)

        if action == ActionTypes.DIARY_REPORT.name:
            return basicDiaryReportQuery.substitute(user_name=object.user_name,
                                                    diary_id=object.diary_id,
                                                    timestamp_start=object.timestamp_start,
                                                    timestamp_end=object.timestamp_end,
                                                    env=env)

        if action == ActionTypes.MEDICATION_SCHEDULE.name:
            return basicMedicationScheduleQuery.substitute(user_name=object.user_name,
                                                           medication_name=object.medication_name,
                                                           effective_start=object.effective_start,
                                                           effective_end=object.effective_end,
                                                           env=env)

        if action == ActionTypes.MEDICATION_REPORT.name or action == ActionTypes.MEDICATION_SKIPPED.name:
            return basicMedicationRerportQuery.substitute(user_name=object.user_name,
                                                          medication_name=object.medication_name,
                                                          report_ts=object.report_ts,
                                                          env=env)

        if action == ActionTypes.TRIGGERED_QUESTIONNAIRE.name:
            return basicQuestionnaireReportSqlQuery.substitute(user_name=object.user_name,
                                                               questionnaire_name=object.triggered_questionnaire,
                                                               questionnaire_timestamp_start=object.triggered_start_time,
                                                               questionnaire_timestamp_end=object.triggered_start_time,
                                                               env=env)

    except KeyError or ValueError:
        return
