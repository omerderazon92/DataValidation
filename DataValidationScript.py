import json
import sys
from Comparator import compare_objects_with_action
from network.NetManager import download_file, get_list_of_zips, scan_athena, define_url
from objects.ObjectsParser import parse_json_file, parse_athena_results
from queries.QueriesManager import create_query, extract_required_actions, ActionTypes

didFailed = False
logs = []
tests_failed = 0
env = sys.argv[1]
FILE_NAME = 1
JSON = 0
delimiter = "----------------" \
            "------------------" \
            "----------------------" \
            "---------------------------" \
            "-------------------------------" \
            "------------------------------------ "
centered_title = "                                "


def fail_increment():
    global tests_failed
    tests_failed += 1


def write_log_file(logs):
    logs_file = "\n".join(logs)
    text_file = open("Logs.txt", "w")
    text_file.write(logs_file)
    text_file.close()

    if didFailed:
        open("Failure", "w")
    else:
        open("Success", "w")
    print(logs_file)
    pass


def main():
    amount_of_validations = 0
    define_url(env)
    zips = get_list_of_zips()
    if zips:
        for zip in zips:
            logs.append(delimiter)
            logs.append( centered_title + "Current Bundle: " + zip)
            # Download the file from the artifactory, list of 1. json 2. file
            jsons_list = download_file(zip)
            for json_file in jsons_list:
                logs.append(delimiter)
                if json_file is None or json_file[JSON] is None or json_file[FILE_NAME] is None:
                    logs.append(
                        json_file[FILE_NAME] + "Couldn't parse  into a JSON file, might be an empty json. moving to "
                                               "the "
                                               "next file...")
                    fail_increment()
                    continue

                # Extract the right action from the JSON file
                actions = extract_required_actions(json.loads(json_file[JSON]))
                if actions is None or len(actions) <= 0:
                    logs.append(json_file[FILE_NAME] + "Didn't get any action to check - actions list might be empty "
                                                       "or "
                                                       "nil")
                    fail_increment()
                    continue

                # Iterates over the actions and validate the right modules
                for action in actions:
                    logs.append("Validating " + json_file[FILE_NAME] + " " + action + ":")
                    if action == ActionTypes.NO_ACTION.name:
                        logs.append("There is no need for validation")
                        continue

                    amount_of_validations = amount_of_validations + 1
                    # Parse the JSON file into an object
                    json_file_object = parse_json_file(json.loads(json_file[JSON]), action)
                    if json_file_object is None:
                        logs.append("Couldn't parse the JSON into an object - moving to the next "
                                    "file...")
                        fail_increment()
                        continue

                    # Extract an Athena query from the object
                    query = create_query(json_file_object, action, env)
                    if query is None:
                        logs.append(
                            "Couldn't extract any query - moving to the next action or file")
                        fail_increment()
                        continue

                    # Scan Athena using a connector and the extracted query
                    results = scan_athena(query, env)
                    if results.empty:
                        logs.append("Couldn't query from athena or got an empty respone, moving to "
                                    "next "
                                    "action or file...(Might be related to the pipeline)")
                        fail_increment()
                        continue

                    # Parse the results into an object
                    athena_results_object = parse_athena_results(results, action)
                    if athena_results_object is None:
                        logs.append("Couldn't parse athena results into an object, moving to "
                                    "the next action "
                                    "or file...")
                        fail_increment()
                        continue

                    # Compare the JSON and Athena results
                    if compare_objects_with_action(action, json_file_object, athena_results_object, logs):
                        logs.append("*Success*")
                    else:
                        didFailed = True
                        logs.append("Expected: (Test Results) " + str(json_file_object))
                        logs.append("Actual: (Server Results) " + str(athena_results_object))
                        fail_increment()

        logs.insert(0,"\n" + str(tests_failed) + "/" + str(amount_of_validations) + " Validations have failed")
    else:
        logs.append("Couldn't get any relevant JSON Zips files to validate - aborting process")
    write_log_file(logs)
    pass


if __name__ == '__main__':
    main()
