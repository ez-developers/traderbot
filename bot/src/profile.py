from bot.utils.request import get
from bot.utils.language import lang
from bot.src.text import t, b
from bot.src.registration import Registration
from telegram import Update
from telegram.ext import CallbackContext


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
        language = lang(chat_id)
        user = get(f'users/{chat_id}')
        status = user['subscription_status']

        if status == True:
            context.bot.send_message(chat_id,
                                     f'{t("expiry_date", language)}: <b>{t("active", language)}</b>', parse_mode='HTML')
        else:
            context.bot.send_message(chat_id,
                                     f'{t("expiry_date", language)}: <b>{t("not_active", language)}</b>', parse_mode='HTML')

    def extend_subscription(self, update: Update, context: CallbackContext):
        return Registration().choose_subscription(update, context, from_profile=True)
