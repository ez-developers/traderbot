from requests.auth import HTTPBasicAuth
from config.settings import API_URL
import requests
from config.settings import API_AUTHENTICATION


def get(API_ENDPOINT: str = None):
    return requests.get(
        API_URL + API_ENDPOINT, auth=API_AUTHENTICATION
    ).json()


def parser(API_URL: str, key: str, API_auth: HTTPBasicAuth = None) -> list:
    custom_list = []
    obj = requests.get(API_URL, auth=API_auth).json()

    for i in obj:
        custom_list.append(i[key])
    return custom_list


def target_video_id(category_name: str) -> int:
    for i in get('video_lessons/'):
        if i["name"] == category_name:
            return i["id"]


def video_list(video_lessons_id: int) -> list:
    output = []
    for i in get('video_lessons/'):
        if i['video_lessons'] == video_lessons_id:
            output.append(i['name'])
    return output


def product_det(product_name: str) -> dict:
    response = requests.get(API_URL + 'products/',
                            auth=API_AUTHENTICATION).json()
    for product in response:
        if product['name'] == product_name:
            return product


def notification_on(chat_id) -> bool:
    user = get(f'users/{chat_id}')
    if user["notifications"]:
        return True
    else:
        return False