from enum import Enum
from string import Template


class AssessmentQueryKeys(Enum):
    ASSESSMENT_NAME = "assessment_name"
    USER_NAME = "user_name"
    STATUS = "assessment_status"
    ASSESSMENT_START_TIME = "assessment_start"
    ASSESSMENT_END_TIME = 'assessment_end'
    TRIGGERED_START_TIME = 'triggered_start_time'
    TRIGGERED_END_TIME = 'triggered_end_time'
    ACTIONS = 'actions'


basicAssessmentReportQuery = Template("""SELECT * FROM "$env"."assessments_steps" 
where user_name  = '$user_name'
and assessment_name = '$assessment_name'
and timestamp '$assessment_start' > assessment_start - interval '30' second
and timestamp '$assessment_start' < assessment_end - interval '30' second
order by assessment_start desc
limit 100;;""")
