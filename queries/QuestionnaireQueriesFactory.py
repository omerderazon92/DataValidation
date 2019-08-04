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


basicQuestionnaireReportSqlQuery = Template("""SELECT * FROM "$env"."questionnaire_report" 
where user_name = '$user_name'
and questionnaire_name = '$questionnaire_name'
and timestamp '$questionnaire_timestamp_start' > questionnaire_timestamp_start - interval '15' second
and timestamp '$questionnaire_timestamp_start'  < questionnaire_timestamp_end - interval '15' second
order by question_order 
limit 100;""")

basicQuestionnaireScheduleQuery = Template("""SELECT * FROM "$env"."questionnaire_schedule" 
where user_name = '$user_name'
and questionnaire_name = '$questionnaire_name'
limit 1;""")

