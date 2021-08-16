from requests.auth import HTTPBasicAuth
from config.settings import API_URL, API_AUTHENTICATION
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
