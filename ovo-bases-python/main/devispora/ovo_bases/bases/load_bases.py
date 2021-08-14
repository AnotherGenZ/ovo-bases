import json
import urllib.request
import os


def load_facilities_remotely():
    url = "http://census.daybreakgames.com/get/ps2/map_region?c:limit=1000&c:show=facility_id,facility_name,facility_type_id,facility_type,zone_id"
    url_open = urllib.request.urlopen(url)
    string_decode = url_open.read().decode('utf-8')
    return json.loads(string_decode)


def determine_source():
    lambda_task_root = os.environ.get('LAMBDA_TASK_ROOT')
    if lambda_task_root is not None:
        return lambda_task_root + '/resources/map_region.json'
    else:
        return os.environ.get('MAP_REGION_LOCATION')


def load_facilities_file():
    returned_source = determine_source()
    with open(returned_source) as map_file:
        return json.load(map_file)
