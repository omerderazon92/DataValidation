def list_comperator(self_list, others_list):
    for index in (0, len(self_list) - 1):
        if self_list[index] != others_list[index]:
            return False
    return True


class QuestionnaireReportResults(object):
    def __init__(self, user_name, questionnaire_name, questionnaire_timestamp_start, questionnaire_timestamp_end,
                 status):
        self.user_name = user_name
        self.questionnaire_name = questionnaire_name
        self.questionnaire_timestamp_start = questionnaire_timestamp_start
        self.questionnaire_timestamp_end = questionnaire_timestamp_end
        self.status = status
        self.questions_answers = []

    def __eq__(self, other):
        return len(self.questions_answers) == len(other.questions_answers) and \
               list_comperator(self.questions_answers, other.questions_answers)

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self):
        return str(self.questions_answers) + " Status" + str(self.status)


class QuestionnaireScheduleResults(object):
    def __init__(self, user_name, questionnaire_name, hour, minute):
        self.user_name = user_name
        self.questionnaire_name = questionnaire_name
        self.hour = hour
        self.hour = minute
