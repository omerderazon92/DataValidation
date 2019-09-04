from string import Template
from enum import Enum


class MedicationQueryKeys(Enum):
    USER_NAME = "user_name"
    MEDICATION_NAME = "medication_name"
    EFFECTIVE_START = "effective_start"
    EFFECTIVE_END = "effective_end"
    STATUS = "status"
    REPORT_TS = "report_ts"
    MEDICATION_TAKEN_TS = "medication_taken_ts"
    HOUR = "hour"
    MINUTE = "minute"
    ACTIONS = "actions"


basicMedicationScheduleQuery = Template("""SELECT * FROM "$env"."medication_schedule" 
where user_name = '$user_name'
and medication_name = '$medication_name'
and effective_end + interval '5' second > timestamp '$effective_end'
and effective_end - interval '7' second < timestamp '$effective_end'
and effective_start + interval '7' second > timestamp '$effective_start'
and effective_start - interval '7' second < timestamp '$effective_start'
limit 100;""")

basicMedicationRerportQuery = Template("""SELECT * FROM "$env"."medication_report"
where user_name = '$user_name'
and medication_name = '$medication_name'
and report_ts + interval '5' second > timestamp '$report_ts'
and report_ts - interval '5' second < timestamp '$report_ts'
limit 10;""")