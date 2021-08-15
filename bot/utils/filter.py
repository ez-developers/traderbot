from telegram.ext import MessageFilter
from bot.src.text import b
from bot.utils.request import parser
from config.settings import API_URL
import json

j = json.load(open("bot/assets/text.json", "r"))


class FilterButton(MessageFilter):
    def __init__(self, section_key: str):
        self.section_key = section_key

    def filter(self, message):
        return message.text in parser(API_URL=f"{API_URL + self.section_key}/",
                                      key="name")


def buttons(key: str):
    button = j["buttons"][key]
    __buttons = []
    for i in button:
        __buttons.append(button[i])
    return '|'.join(j for j in __buttons)
