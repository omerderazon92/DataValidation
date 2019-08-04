from datetime import date

from network.Preprod import get_list_of_files, download_file, scan_athena
from objects.ObjectsParser import parse_json_file, parse_athena_results
from queries.QueriesManager import ActionTypes, create_query, extract_required_actions

logs = []
tests_failed = 0
date = date.today()


def add_log(log):
    global logs
    logs.append(log)


def report_fail():
    global tests_failed
    tests_failed += 1


def compare_objects_with_action(action, json_file_object, athena_results_object):
    if action == ActionTypes.QUESTIONNAIRE_REPORT.name:
        if len(json_file_object.questions_answers) != len(athena_results_object.questions_answers):
            return False
        else:
            for index in range(0, len(athena_results_object.questions_answers)):
                if athena_results_object.questions_answers[index] != json_file_object.questions_answers[index]:
                    return False
            if json_file_object.status != athena_results_object.status:
                return False
        return True
    if action == ActionTypes.QUESTIONNAIRE_SCHEDULE.name:
        if json_file_object.hour != athena_results_object.hour or json_file_object.minute != athena_results_object.minute:
            return False
        return True
    if action == ActionTypes.ASSESSMENT_REPORT.name:
        if json_file_object.assessment_name != athena_results_object.assessment_name or json_file_object.status != athena_results_object.status:
            return False
        return True
    if action == ActionTypes.GYRO_DATA.name:
        if athena_results_object.actual / athena_results_object.expected < 0.95:
            return False
        return True
    if action == ActionTypes.DIARY_REPORT.name:
        if len(json_file_object.answers) != len(athena_results_object.answers):
            return False
        else:
            for index in range(0, len(athena_results_object.answers)):
                if athena_results_object.answers[index] != json_file_object.answers[index]:
                    return False
            if json_file_object.status != athena_results_object.status:
                return False
        return True
    pass


def main():
    raw_files = get_list_of_files()
    if raw_files:
        for file_name in raw_files:
            # Download the file from the artifactory
            loaded_json = download_file(file_name)
            if loaded_json is None:
                add_log(
                    file_name + " Couldn't parse  into a JSON file, might be empty json. moving to the next file...")
                report_fail()
                continue

            # Extract the right action from the JSON file
            actions = extract_required_actions(loaded_json)
            if actions is None or len(actions) <= 0:
                add_log(file_name + " Didn't get any action to check - actions list might be empty or nil")
                report_fail()
                continue

            # Iterates over the actions and validate the right modules
            for action in actions:
                # Parse the JSON file into an object
                json_file_object = parse_json_file(loaded_json, action)
                if json_file_object is None:
                    add_log(file_name + " Couldn't parse the JSON into an object - moving to the next file...")
                    report_fail()
                    continue

                # Extract an Athena query from the object
                query = create_query(json_file_object, action)
                if query is None:
                    add_log(file_name + " Couldn't extract any query - moving to the next action or file")
                    report_fail()
                    continue

                # Scan Athena using a connector and the extracted query
                results = scan_athena(query)
                if results.empty:
                    add_log(file_name + " Couldn't query from athena or got an empty results, moving to next "
                                        "action or file...")
                    report_fail()
                    continue

                # Parse the results into an object
                athena_results_object = parse_athena_results(results, action)
                if athena_results_object is None:
                    add_log(file_name + " Couldn't parse athena DB results into an object, moving to the next action "
                                        "or file...")
                    report_fail()
                    continue

                # Compare the JSON and Athena results
                if compare_objects_with_action(action, json_file_object, athena_results_object):
                    add_log(file_name + " With " + action + " checking Has Passed successfully")
                else:
                    add_log(file_name + " With " + action + " Has Failed")
                    add_log(file_name + " Expected: " + str(json_file_object))
                    add_log(file_name + " Actual    " + str(athena_results_object))
                    report_fail()

        logs.append(str(tests_failed) + "/" + str(len(raw_files)) + " Has failed")

    else:
        add_log("Couldn't get any relevant JSON files to validate - aborting process")

    print("\n".join(logs))
    pass


if __name__ == '__main__':
    main()
