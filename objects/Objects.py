class QuestionnaireReportResults(object):
    def __init__(self, user_name, questionnaire_name, actions="", questionnaire_timestamp_start="",
                 questionnaire_timestamp_end="", status="", hour="", minute=""):
        self.user_name = user_name
        self.questionnaire_name = questionnaire_name
        self.actions = actions
        self.questionnaire_timestamp_start = questionnaire_timestamp_start
        self.questionnaire_timestamp_end = questionnaire_timestamp_end
        self.status = status
        self.answers = []
        self.hour = hour
        self.minute = minute

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self):
        meta_data = self.user_name + " " + self.questionnaire_name

        if len(self.answers) > 0:
            meta_data = meta_data + " Answers: " + str(self.answers)
        if self.status is not None:
            meta_data = meta_data + " Status: " + self.status
        if self.hour is not None and self.minute is not None:
            meta_data = meta_data + " Hour: " + self.hour + " Minute: " + self.minute
        return meta_data


class AssessmentReportResults(object):
    def __init__(self, user_name, assessment_name, actions="", assessment_start="",
                 assessment_end="", triggered_start_time="", triggered_end_time="", status=""):
        self.user_name = user_name
        self.assessment_name = assessment_name
        self.actions = actions
        self.assessment_start = assessment_start
        self.assessment_end = assessment_end
        self.triggered_start_time = triggered_start_time
        self.triggered_end_time = triggered_end_time
        self.status = status

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self):
        meta_data = self.user_name + " " + self.assessment_name + " Status: " + self.status
        return meta_data


class AssessmentDataValidation(object):
    def __init__(self, user_name, assessment_id, actual, expected):
        self.user_name = user_name
        self.assessment_id = assessment_id
        self.actual = actual
        self.expected = expected

    def __hash__(self):
        return super.__hash__()

    def __repr__(self):
        meta_data = "Actual samples rate: " + str(self.actual) + "  expected samples rate: " + str(
            self.expected) + " which " \
                             "means: " + str(self.actual / self.expected)
        return meta_data


class DiaryReportResults(object):
    def __init__(self, user_name, diary_id, actions="", timestamp_start="",
                 timestamp_end="", status=""):
        self.user_name = user_name
        self.diary_id = diary_id
        self.actions = actions
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.status = status
        self.answers = []

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self):
        meta_data = self.user_name + " " + self.diary_id

        if len(self.answers) > 0:
            meta_data = meta_data + " Answers: " + str(self.answers)
        if self.status is not None:
            meta_data = meta_data + " Status: " + self.status
        return meta_data


class MedicationReportResults(object):
    def __init__(self, user_name, medication_name, actions="", effective_start="",
                 effective_end="", status="", medication_taken_ts="", report_ts="", hour="", minute=""):
        self.user_name = user_name
        self.medication_name = medication_name
        self.actions = actions
        self.effective_start = effective_start
        self.effective_end = effective_end
        self.status = status
        self.medication_taken_ts = medication_taken_ts
        self.report_ts = report_ts
        self.hour = hour
        self.minute = minute

    def __repr__(self):
        meta_data = "Medication name: " + self.medication_name

        if self. effective_start is not  None and self.effective_end is not None:
            meta_data = " Effective start: " + str(self.effective_start) + " Effective end: " + str(self.effective_end)
        if self. hour is not None and self.minute is not None:
            meta_data = meta_data + " Hour: " + str(self.hour) + " Minute: " + str(self.minute)
        if self.status is not None:
            meta_data = meta_data + " Status: " + self.status
        if self.medication_taken_ts is not None:
            meta_data = meta_data + " Medication taken ts: " + str(self.medication_taken_ts)
        return meta_data
