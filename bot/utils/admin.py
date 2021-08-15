
from config.settings import ADMIN_IDS


def is_admin(chat_id):
    if chat_id in ADMIN_IDS:
        return True
    else:
        return False
