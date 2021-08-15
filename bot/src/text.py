import json

j = json.load(open("bot/assets/text.json", "r"))


def t(key: str, lang: str):
    """b Function that gets the text for the bot from text.json

    Args:
        key (str): [key for the json to find the right piece of text]
        lang (str): [language of the given text]

    Returns:
        [str]: [Text from text.json]
    """
    return j["texts"][key][lang]


def b(key: str, lang: str):
    """b Function that gets the text of a button in the bot from text.json

    Args:
        key (str): [key for the json to find the right piece of text]
        lang (str): [language of the given text]

    Returns:
        [str]: [Text from text.json]
    """
    return j["buttons"][key][lang]
