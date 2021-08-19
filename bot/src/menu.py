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
from bot.utils.request import get, parser
from bot.utils.build_menu import build_menu
import logging


class Menu:

    def display(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "MENU_DISPLAYED"
        menu_buttons = [
            [KeyboardButton(b("my_profile", language)),
             KeyboardButton(b("videos", language))],
            [KeyboardButton(b("support", language)),
             KeyboardButton(b("portfolio", language))]
        ]

        context.bot.send_message(chat_id,
                                 t("main_page", language),
                                 reply_markup=ReplyKeyboardMarkup(
                                     menu_buttons, resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"{chat_id} - opened main menu. Returned state: {state}")
        return state

    def my_profile(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "MY_PROFILE"
        markup = [
            [KeyboardButton(b("my_info", language)),
             KeyboardButton(b("subscription_status", language))],
            [KeyboardButton(b("extend_subscription", language)),
             KeyboardButton(b("back", language))]
        ]

        context.bot.send_message(chat_id,
                                 f'<b>{t("your_profile", language)}</b>',
                                 reply_markup=ReplyKeyboardMarkup(
                                     markup, resize_keyboard=True),
                                 parse_mode='HTML')

        logging.info(f"{chat_id} - opened my profile. Returned state: {state}")
        return state

    def video_lessons(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "VIDEOS"
        video_list = parser('videos/', 'name')

        context.bot.send_message(chat_id,
                                 f'<b>{t("video_lessons", language)}</b>',
                                 reply_markup=ReplyKeyboardMarkup(
                                     build_menu(
                                         buttons=[
                                             KeyboardButton(s) for s in video_list
                                         ],
                                         n_cols=1,
                                         footer_buttons=[
                                             KeyboardButton(
                                                 b("back", language))
                                         ]), resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"{chat_id} - want to watch one of the video lessons. Returned state: {state}")
        return state

    def portfolio(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "PORTFOLIOS"
        portfolio_list = parser('portfolios/', 'name')

        context.bot.send_message(chat_id,
                                 f'<b>{t("portfolios_display", language)}</b>',
                                 reply_markup=ReplyKeyboardMarkup(
                                     build_menu(
                                         buttons=[
                                             KeyboardButton(s) for s in portfolio_list
                                         ],
                                         n_cols=1,
                                         footer_buttons=[KeyboardButton(b("back", language))]), resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(f"{chat_id} - opened portfolios. Returned state: {state}")
        return state

    def support(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "SUPPORT"
        markup = [
            [KeyboardButton(b("back", language))]
        ]

        context.bot.send_message(chat_id,
                                 t("request_question", language),
                                 reply_markup=ReplyKeyboardMarkup(
                                     markup, resize_keyboard=True),
                                 parse_mode='HTML')

        logging.info(
            f"{chat_id} - is requesting support. Returned state: {state}")
        return state
