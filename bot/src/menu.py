from telegram import (ReplyKeyboardMarkup,
                      Update,
                      KeyboardButton,
                      ChatAction,
                      InputMediaPhoto,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import CallbackContext
from bot.src.text import t, b
from bot.utils.language import lang
from bot.utils.request import get
from bot.utils.build_menu import build_menu
import logging


class Menu:

    def display(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "MENU_DISPLAYED"
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

    def my_profile(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "MY_PROFILE"
        markup = [
            [KeyboardButton(b("user_name", lang(chat_id)))],
            [KeyboardButton(b("subscription_status", lang(chat_id)))],
            [KeyboardButton(b("pay", lang(chat_id)))],
            [KeyboardButton(b("back", lang(chat_id)))]
        ]

        context.bot.send_message(chat_id,
                                 "Welcome to your personal profile",
                                 reply_markup=ReplyKeyboardMarkup(
                                     markup, resize_keyboard=True),
                                 parse_mode='HTML')

        logging.info(f"{chat_id} - opened my profile. Returned state: {state}")
        return state
    
    
    def portfolio(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "PORTFOLIOS"
        portfolio_list = [].append(i['name'] for i in get('portfolios/'))
        
        context.bot.send_message(chat_id,
                                 f'{t("portfolio", lang(chat_id))}',
                                 reply_markup=ReplyKeyboardMarkup(
                                 build_menu(
                                     buttons=[KeyboardButton(s) for s in portfolio_list],
                                     n_cols = 1,
                                     footer_buttons=[
                                         KeyboardButton(b("back", lang(chat_id)))
                                     ], resize_keyboard=True))
                                 )
