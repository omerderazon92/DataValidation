from enum import Enum

from queries.AssessmentQueriesFactory import basicAssessmentReportQuery
from queries.QuestionnaireQueriesFactory import basicQuestionnaireReportSqlQuery, basicQuestionnaireScheduleQuery, \
    QuestionnaireQueryKeys
from queries.DiaryQueriesFactory import basicDiaryReportQuery
from queries.WatchDataQueryFactory import basicGyroQuery


class ActionTypes(Enum):
    QUESTIONNAIRE_REPORT = "0"
    QUESTIONNAIRE_SCHEDULE = "1"
    ASSESSMENT_REPORT = "2"
    GYRO_DATA = "3"
    DIARY_REPORT = "4"


def extract_required_actions(loaded_json):
    try:
        return loaded_json[QuestionnaireQueryKeys.ACTIONS.value]
    except KeyError or ValueError:
        return


def create_query(object, action):
    try:
        if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
            return basicQuestionnaireReportSqlQuery.substitute(user_name=object.user_name,
                                                               questionnaire_name=object.questionnaire_name,
                                                               questionnaire_timestamp_start=object.questionnaire_timestamp_start,
                                                               questionnaire_timestamp_end=object.questionnaire_timestamp_end)
        if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
            return basicQuestionnaireScheduleQuery.substitute(user_name=object.user_name,
                                                              questionnaire_name=object.questionnaire_name,
                                                              )
        if action == ActionTypes.ASSESSMENT_REPORT.name:
            return basicAssessmentReportQuery.substitute(user_name=object.user_name,
                                                         assessment_name=object.assessment_name,
                                                         assessment_start=object.assessment_start,
                                                         assessment_end=object.assessment_end)

        if action == ActionTypes.GYRO_DATA.name:
            return basicGyroQuery.substitute(user_name=object.user_name,
                                             assessment_end=object.assessment_end)

        if action == ActionTypes.DIARY_REPORT.name:
            return basicDiaryReportQuery.substitute(user_name=object.user_name,
                                                    diary_id=object.diary_id,
                                                    timestamp_start=object.timestamp_start)
    except KeyError or ValueError:
        return
