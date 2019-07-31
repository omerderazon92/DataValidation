from string import Template
from enum import Enum

articfactory_adress = 'http://aa-artifactory.intel.com:8081/artifactory/health-snapshot-local/com/intel/aa/validation_files/'


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


class AssessmentQueryKeys(Enum):
    ASSESSMENT_NAME = "assessment_name"
    USER_NAME = "user_name"
    STATUS = "assessment_status"
    ASSESSMENT_START_TIME = "assessment_start"
    ASSESSMENT_END_TIME = 'assessment_end'
    TRIGGERED_START_TIME = 'triggered_start_time'
    TRIGGERED_END_TIME = 'triggered_end_time'
    ACTIONS = 'actions'


class WatchDataQueryKeys(Enum):
    ACTUAL = "actual_acc_records"
    EXPECTED = "expected_acc_records"
    ASSESSMENT_ID = "assessment_report_id"
    USER_NAME = "user_name"


class ActionTypes(Enum):
    QUESTIONNAIRE_REPORT = "0"
    QUESTIONNAIRE_SCHEDULE = "1"
    ASSESSMENT_REPORT = "2"
    GYRO_DATA = "3"


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

basicAssessmentReportQuery = Template("""SELECT * FROM "kclprep"."assessments_steps" 
where user_name  = '$user_name'
and assessment_name = '$assessment_name'
and assessment_start = timestamp '$assessment_start'
and assessment_end = timestamp '$assessment_end'
limit 100;""")

basicGyroQuery = Template("""SELECT NEW.user_name,
                NEW.assessment_report_id,
                NEW.assessment_name,
                NEW. expected_vs_actual,
                NEW.actual_acc_records,
                NEW.expected_acc_records,
                NEW.step_start,
                NEW.assessment_end,
                NEW.assessment_duration_second
                FROM
                (SELECT A_S.user_id,
                A_S.user_name,
                assessment_report_id,
                assessment_name,
                step_start,
                assessment_end,
                count(timestamp) actual_acc_records,
                assessment_duration_second*(50) expected_acc_records,
                (count(timestamp)) / (assessment_duration_second*(50.0)) expected_vs_actual,
                assessment_duration_second
                FROM
                (SELECT user_id,
                user_name,
                assessment_report_id,
                assessment_name,
                assessment_start,
                assessment_end,
                step_start,
                date_diff('Second', min(step_start),max(assessment_end)) assessment_duration_second
                FROM "assessments_steps"
                where step_name='Stand with arms at rest'
                and assessment_end = timestamp '$assessment_end'
                GROUP BY user_id, user_name, assessment_report_id, assessment_name, assessment_start, assessment_end ,step_start ) A_S
                LEFT JOIN
                (SELECT user_id,
                timestamp
                FROM acc_gyro
                WHERE measurement_name='Watch Gyroscope'
                and timestamp>= (current_date - interval '5' day)
                ) A_G
                ON A_S.user_id=A_G.user_id
                AND A_G.timestamp>=A_S.assessment_start
                AND A_G.timestamp<=A_S.assessment_end
                GROUP BY A_S.user_id, A_S.user_name, assessment_report_id, assessment_name, assessment_duration_second,
                assessment_start, assessment_end , step_start )new
                WHERE user_name like '$user_name'
                ORDER BY step_start desc""")


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
    if action == ActionTypes.ASSESSMENT_REPORT.name:
        return basicAssessmentReportQuery.substitute(user_name=object.user_name,
                                                     assessment_name=object.assessment_name,
                                                     assessment_start=object.assessment_start,
                                                     assessment_end=object.assessment_end)

    if action == ActionTypes.GYRO_DATA.name:
        return basicGyroQuery.substitute(user_name=object.user_name,
                                         assessment_end=object.assessment_end)
