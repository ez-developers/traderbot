from telegram.ext import MessageFilter
from bot.utils._reqs import parser
from config.settings import API_URL, API_AUTHENTICATION
from requests.auth import HTTPBasicAuth
import json

j = json.load(open("bot/assets/text.json", "r"))


class FilterButton(MessageFilter):
    def __init__(self, section_key: str):
        self.section_key = section_key

    def filter(self, message):
        return message.text in parser(API_URL=f"{API_URL + self.section_key}/",
                                      API_auth=API_AUTHENTICATION,
                                      key="name")