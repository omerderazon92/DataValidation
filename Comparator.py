from queries.QueriesManager import ActionTypes


def compare_objects_with_action(action, json_file_object, athena_results_object, logs):
    if action == ActionTypes.QUESTIONNAIRE_REPORT.name or action == ActionTypes.DIARY_REPORT.name:
        if len(json_file_object.answers) != len(athena_results_object.answers):
            logs.append("*Failed* different amount of answers")
            return False
        else:
            for index in range(0, len(athena_results_object.answers)):
                if athena_results_object.answers[index] != json_file_object.answers[index]:
                    logs.append("*Failed* answer " + str(index + 1) + " is different")
                    return False
            if json_file_object.status != athena_results_object.status:
                return False
        return True
    if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
        if json_file_object.hour != athena_results_object.hour or json_file_object.minute != athena_results_object.minute:
            logs.append("*Failed*")
            return False
        return True
    if action == ActionTypes.ASSESSMENT_REPORT.name:
        if str(json_file_object.numeber_of_steps) != str(athena_results_object.numeber_of_steps):
            logs.append("*Differet amount of steps")
            return False
        else:
            if json_file_object.assessment_name != athena_results_object.assessment_name or json_file_object.status != athena_results_object.status:
                logs.append("*Failed*")
                return False
        return True
    if action == ActionTypes.GYRO_DATA.name:
        gyro_treshold = 0.95
        if athena_results_object.actual / athena_results_object.expected < gyro_treshold:
            logs.append("*Failed*")
            return False
        return True
    if action == ActionTypes.MEDICATION_SCHEDULE.name:
        if json_file_object.hour != athena_results_object.hour or json_file_object.minute != athena_results_object.minute:
            logs.append("*Failed*")
            return False
        return True
    if action == ActionTypes.MEDICATION_REPORT.name:
        if str(json_file_object.medication_taken_ts) != str(athena_results_object.medication_taken_ts) or json_file_object.status != athena_results_object.status:
            logs.append("*Failed*")
            return False
        return True
    if action == ActionTypes.MEDICATION_SKIPPED.name:
        if json_file_object.status != athena_results_object.status:
            logs.append("*Failure*")
            return False
        return True
    if action == ActionTypes.TRIGGERED_QUESTIONNAIRE.name:
        return True
    pass
