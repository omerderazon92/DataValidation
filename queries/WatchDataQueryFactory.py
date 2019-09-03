from enum import Enum
from string import Template


class WatchDataQueryKeys(Enum):
    ACTUAL = "actual_acc_records"
    EXPECTED = "expected_acc_records"
    ASSESSMENT_ID = "assessment_report_id"
    USER_NAME = "user_name"


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
                and assessment_end + interval '5' second > timestamp '$assessment_end'
                and assessment_end - interval '5' second < timestamp '$assessment_end'
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
