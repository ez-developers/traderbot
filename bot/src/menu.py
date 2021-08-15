from telegram import (ReplyKeyboardMarkup,
                      Update,
                      KeyboardButton,
                      ChatAction,
                      InputMediaPhoto,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import CallbackContext
from bot.src.text import t, b
from bot.utils.build_menu import build_menu
from bot.utils.language import lang
from bot.utils.request import (parser,
                               target_category_id,
                               products_list,
                               product_det,
                               notification_on,
                               get)
from config.settings import API_URL, API_AUTHENTICATION, BASE_DIR, GROUP_ID
import logging
import time
import json
import requests

j = json.load(open("bot/assets/text.json", "r"))
text = j["texts"]
button = j["buttons"]
menu_button = j["buttons"]


class Menu:

    def display(self, update: Update, context: CallbackContext):
        state = "MENU_DISPLAYED"
        chat_id = update.effective_chat.id
        menu_buttons = [
            [KeyboardButton(b("my_profile", lang(chat_id))),
             KeyboardButton(b("video_lessons", lang(chat_id)))],
            [KeyboardButton(b("support", lang(chat_id))),
             KeyboardButton(b("portfolios", lang(chat_id)))]
        ]

        context.bot.send_message(chat_id,
                                 t("main_page", lang(chat_id)),
                                 reply_markup=ReplyKeyboardMarkup(
                                     menu_buttons, resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"{chat_id} - opened main menu. Returned state: {state}")
        return state
