class QuestionnaireReportResults(object):
    def __init__(self, user_name, questionnaire_name, actions="", questionnaire_timestamp_start="",
                 questionnaire_timestamp_end="", status="", hour="", minute=""):
        self.user_name = user_name
        self.questionnaire_name = questionnaire_name
        self.actions = actions
        self.questionnaire_timestamp_start = questionnaire_timestamp_start
        self.questionnaire_timestamp_end = questionnaire_timestamp_end
        self.status = status
        self.questions_answers = []
        self.hour = hour
        self.minute = minute

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self):
        meta_data = self.user_name + " " + self.questionnaire_name

        if len(self.questions_answers) > 0:
            meta_data = meta_data + " Answers: " + str(self.questions_answers)
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
        meta_data = "Actual samples rate: " + str(self.actual) + "  expected samples rate: " + str(self.expected) + " which " \
             "means: " + str(self.actual / self.expected)
        return meta_data
