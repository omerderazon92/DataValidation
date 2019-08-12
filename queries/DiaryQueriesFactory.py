from enum import Enum
from string import Template


class DiaryQueryKeys(Enum):
    DIARY_TIMESTAMP_START = "timestamp_start"
    DIARY_TIMESTAMP_END = "timestamp_end"
    DIARY_ID = "diary_id"
    USER_NAME = "user_name"
    STATUS = "status"
    ANSWER = "answer"
    ACTIONS = "actions"


basicDiaryReportQuery = Template("""SELECT * FROM "$env"."diary_report" 
where user_name = '$user_name'
and diary_id = '$diary_id'
and timestamp '$timestamp_start'  > timestamp_start - interval '1' minute
and timestamp '$timestamp_start' < timestamp_start +1 interval '1' minute
order by question_order desc
limit 100;""")
