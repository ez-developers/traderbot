import json

j = json.load(open("bot/assets/text.json", "r"))


def t(key: str, lang="ru"):
    return j["texts"][key][lang]


def b(key: str, lang="ru"):
    return j["buttons"][key][lang]
