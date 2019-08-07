import re
from enum import Enum
from io import BytesIO
from zipfile import ZipFile

import pandas as pd
import requests
from pyathenajdbc import connect

base_url = 'http://aa-artifactory.intel.com:8081/artifactory/health-snapshot-local/com/intel/aa/validation_files/jobUploadOmer7/'
target_url = ""


class Env(Enum):
    KCL_PREP = "kclprep"
    KCL_TEST = "test"


def define_env(env):
    global target_url
    if env == Env.KCL_TEST.value:
        target_url = base_url + "Test/"
    elif env == Env.KCL_PREP.value:
        target_url = base_url + "Preprod/"


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


def get_list_of_zips():
    files = []
    response = requests.get(target_url, auth=('jenkins', 'jenkins123!'))
    if response:
        response_content = str(response.content)
        if response_content:
            for match in re.finditer(">jsonFiles_[0-9]*.zip", response_content):
                files.append(match.group(0).replace(">", ''))
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
            target_url + file_name,
            auth=('jenkins', 'jenkins123!'))
        if response:
            return extract_json_from_zip(response.content)

    except ValueError:
        return
