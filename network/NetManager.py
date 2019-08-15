import re
from enum import Enum
from io import BytesIO
from zipfile import ZipFile

import pandas as pd
import requests
from pyathenajdbc import connect
from datetime import date, timedelta

base_url = 'http://aa-artifactory.intel.com:8081/artifactory/health-snapshot-local/com/intel/aa' \
           '/BDD_DATA_VALIDATION_TESTS/'


class Env(Enum):
    KCL_PREP = "kclprep"
    KCL_TEST = "test"
    SHEBA_TEST = 'shebatest'


def define_url(env):
    global base_url
    if env == Env.KCL_TEST.value:
        base_url = base_url + "KCL/Test/"
    elif env == Env.KCL_PREP.value:
        base_url = base_url + "KCL/Preprod/"
    elif env == Env.KCL_TEST.value:
        base_url = base_url + "Sheba/ShebaTest/"

    yesterday = date.today() - timedelta(days=1)
    base_url = base_url + str(yesterday.month - 1) + "/"
    base_url = base_url + str(yesterday.day) + "/"
    print(base_url)


def scan_athena(query, env):
    if env == Env.KCL_PREP.value:
        conn = connect(profile_name='health-customers',
                       s3_staging_dir='s3://aws-athena-query-results-eu-west-1-036573440528/',
                       region_name='eu-west-1',
                       schema_name='kclprep')
        return pd.read_sql(query, conn)
    if env == Env.KCL_TEST.value:
        conn = connect(profile_name='health',
                       s3_staging_dir='s3://aws-athena-query-results-458907533143-us-west-2/',
                       region_name='us-west-2',
                       schema_name='test')
        return pd.read_sql(query, conn)
    if env == Env.SHEBA_TEST.value:
        conn = connect(profile_name='health',
                       s3_staging_dir='s3://aws-athena-query-results-458907533143-us-west-2/',
                       region_name='us-west-2',
                       schema_name='shebatest')
        return pd.read_sql(query, conn)


def get_list_of_zips():
    files = []
    json_file_pattern = "[a-zA-Z]*-debug-[a-zA-Z]*_[a-zA-Z]*_jsonFiles_[0-9]*.zip<"
    response = requests.get(base_url, auth=('jenkins', 'jenkins123!'))
    if response:
        response_content = str(response.content)
        if response_content:
            for match in re.finditer(json_file_pattern, response_content):
                files.append(match.group(0).replace("<", ''))
            return files


def extract_json_from_zip(content):
    jsons_list = []
    zipfile = ZipFile(BytesIO(content))
    for f in zipfile.namelist():
        json = zipfile.open(f)
        string_json = str(json.read())
        string_json = string_json[2:]
        string_json = string_json[:len(string_json) - 1]
        jsons_list.append((string_json.replace('\\n', ''), f))
    return jsons_list


def download_file(file_name):
    try:
        response = requests.get(
            base_url + file_name,
            auth=('jenkins', 'jenkins123!'))
        if response:
            return extract_json_from_zip(response.content)

    except ValueError:
        return
