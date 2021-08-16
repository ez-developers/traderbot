from bot.utils.request import get
from bot.utils.language import lang
from bot.src.text import t, b
from telegram import Update
from telegram.ext import CallbackContext


class Profile():

    def my_info(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        user = get(f"users/{chat_id}/")
        
        context.bot.send_message(chat_id, 
                                 user)

    def subscription_status(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        user = get(f'users/{chat_id}/')
        status = user['subscription_status']
        
        if status == True:
            context.bot.send_message(chat_id,
                                     f'{t("expiry_date", language) + ": " + t("active", language)}')
        else:
            context.bot.send_message(chat_id,
                                     f'{t("expiry_date", language) + ": " + t("not_active", language)}')