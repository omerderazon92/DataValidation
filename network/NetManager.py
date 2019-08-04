from enum import Enum

import pandas as pd
import requests
from pyathenajdbc import connect
import re


class Enviroments(Enum):
    KCL_PREP = "kclprep"


articfactory_base_url = 'http://aa-artifactory.intel.com:8081/artifactory/health-snapshot-local/com/intel/aa/validation_files/'


def scan_athena(query, env):
    if env == Enviroments.KCL_PREP.value:
        conn = connect(profile_name='health-customers',
                       s3_staging_dir='s3://aws-athena-query-results-eu-west-1-036573440528/',
                       region_name='eu-west-1',
                       schema_name='kclprep')
        return pd.read_sql(query, conn)


def get_list_of_files():
    files = []
    response = requests.get(articfactory_base_url, auth=('jenkins', 'jenkins123!'))
    if response:
        response_content = str(response.content)
        if response_content:
            for match in re.finditer('href="BDD(.+?)json', response_content):
                files.append(match.group(0).replace("href=\"", ''))
            return files


def download_file(file_name):
    try:
        response = requests.get(
            articfactory_base_url + file_name,
            auth=('jenkins', 'jenkins123!'))
        if response:
            if response.json():
                return response.json()
    except ValueError:
        return
