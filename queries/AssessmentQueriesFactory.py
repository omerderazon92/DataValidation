from enum import Enum
from string import Template


class AssessmentQueryKeys(Enum):
    ASSESSMENT_NAME = "assessment_name"
    USER_NAME = "user_name"
    STATUS = "assessment_status"
    ASSESSMENT_START_TIME = "assessment_start"
    ASSESSMENT_END_TIME = 'assessment_end'
    TRIGGERED_START_TIME = 'triggered_start'
    TRIGGERED_END_TIME = 'triggered_end'
    ACTIONS = 'actions'
    NUMBER_OF_STEPS = 'numeber_of_steps'
    TRIGGERED_QUESTIONNAIRE = 'triggered_questionnaire'
    TRIGGERED_QUESTIONNAIRE_START = 'questionnaire_timestamp_start'
    TRIGGERED_QUESTIONNAIRE_END = 'questionnaire_timestamp_end'
    TRIGGERED_QUESTIONNAIRE_NAME = 'questionnaire_name'


basicAssessmentReportQuery = Template("""SELECT * FROM "$env"."assessments_steps" 
where user_name  = '$user_name'
and assessment_name = '$assessment_name'
and timestamp '$assessment_start' > assessment_start - interval '1' minute
and timestamp '$assessment_end' < assessment_end + interval '1' minute
order by assessment_start desc
limit 100;;""")

basicTappingReportQuery = Template ("""SELECT * FROM "$env"."assessments_tapping" 
where user_name = '$user_name'
limit 100;""")
