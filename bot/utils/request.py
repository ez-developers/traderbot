from requests.auth import HTTPBasicAuth
from core.settings import API_URL, API_AUTHENTICATION
import requests


def get(API_ENDPOINT: str = None):
    return requests.get(
        API_URL + API_ENDPOINT + '/', auth=API_AUTHENTICATION
    ).json()


def post(API_ENDPOINT: str, data):
    return requests.post(
        API_URL + API_ENDPOINT, auth=API_AUTHENTICATION, json=data
    ).json()


def put(API_ENDPOINT: str, data):
    return requests.put(
        API_URL + API_ENDPOINT, auth=API_AUTHENTICATION, json=data
    ).json()


def parser(API_ENDPOINT: str, key: str):
    custom_list = []
    obj = requests.get(API_URL + API_ENDPOINT, auth=API_AUTHENTICATION).json()

    for i in obj:
        custom_list.append(i[key])
    return custom_list


def get_target_id_by_name(API_ENDPOINT: str, target: str):
    """
    Parses data from the target API endpoint and gets the id of the requested target. 

    Args:
        API_ENDPOINT (str): URL to get the object
        target (str): "name" field of the requested object
    """
    object = get(API_ENDPOINT)

    for i in object:
        if i['name'] == target:
            return i['id']
