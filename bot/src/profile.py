from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from bot.utils.request import get
from bot.utils.language import lang
from bot.src.text import t, b
from bot.src.registration import Registration
import datetime
import locale
import logging


class Profile():

    def my_info(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        user = get(f"users/{chat_id}")

        context.bot.send_message(chat_id,
                                 f"{t('my_info', language)}"
                                 .format(
                                     user['id'],
                                     user['first_name'],
                                     user['last_name'] if user['last_name'] is not None else "-",
                                     user['phone_number']
                                 ), parse_mode='HTML')

    def subscription_status(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        user = get(f'users/{chat_id}')
        language = user['language']
        status = user['subscription_status']
        locale.setlocale(locale.LC_TIME, f'{language}_{language.upper()}')
        date = datetime.datetime.strptime(
            user['subscribed_until'], "%Y-%m-%d").strftime('%d %B %Y')

        if status == True:
            context.bot.send_message(chat_id,
                                     f'{t("subscription_status", language)}: <b>{t("active", language)}</b>\n{t("expiry_date", language)}: <b>{date}</b>', parse_mode='HTML')
        else:
            context.bot.send_message(chat_id,
                                     f'{t("subscription_status", language)}: <b>{t("not_active", language)}</b>', parse_mode='HTML')

    def extend_subscription(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        markup = [
            [
                KeyboardButton(b('1_year', language)),
                KeyboardButton(b('3_years', language)),
                KeyboardButton(b('5_years', language)),
            ],
            [KeyboardButton(b('back', language))]
        ]
        state = "CHOOSING_PLANS"

        context.bot.send_message(chat_id,
                                 t('choosing_plans', language),
                                 reply_markup=ReplyKeyboardMarkup(markup,
                                                                  resize_keyboard=True),
                                 parse_mode='HTML')

        logging.info(
            f"{chat_id} - is extending his subscription. Returned state: {state}")
        return state
