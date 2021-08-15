from .request import get


def lang(chat_id):
    user = get(f'users/{chat_id}')
    return user['language']
