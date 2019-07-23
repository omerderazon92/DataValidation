from string import Template
from enum import Enum


class QuestionnaireQueryKeys(Enum):
    QUESTIONNAIRE_TIMESTAMP_START = "questionnaire_timestamp_start"
    QUESTIONNAIRE_TIMESTAMP_END = "questionnaire_timestamp_end"
    QUESTIONNAIRE_NAME = "questionnaire_name"
    USER_NAME = "user_name"
    STATUS = "status"
    ANSWER = "answer"
    HOUR = "hour"
    MINUTE = "minute"
    ACTIONS = "actions"


class ActionTypes(Enum):
    QUESTIONNAIRE_REPORT = "0"
    QUESTIONNAIRE_SCHEDULE = "1"


basicQuestionnaireReportSqlQuery = Template("""SELECT * FROM "kcl"."questionnaire_report" 
where user_name = '$user_name'
and questionnaire_name = '$questionnaire_name'
and questionnaire_timestamp_start = timestamp '$questionnaire_timestamp_start'
and questionnaire_timestamp_end = timestamp '$questionnaire_timestamp_end' 
order by question_order 
limit 100;""")

basicQuestionnaireScheduleQuery = Template("""SELECT * FROM "kcl"."questionnaire_schedule" 
where user_name = '$user_name'
and questionnaire_name = '$questionnaire_name'
limit 1;""")
