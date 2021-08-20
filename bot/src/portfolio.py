from telegram import Update, chat
from telegram.ext import CallbackContext
from bot.utils.request import get, put, get_target_id_by_name
from bot.utils.language import lang
from bot.src.text import t
import time


class Portfolio():

    def handle_portfolio_click(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        id = get_target_id_by_name('portfolios', update.message.text)
        all_users = []

        portfolio = get(f'portfolios/{id}')

        for i in portfolio['users_list']:
            all_users.append(i)

        if chat_id in all_users:
            update.effective_message.reply_text(
                "you are already on the portfolio")
            return
        else:
            all_users.append(chat_id)

        payload = {
            "users_list": all_users,
            "users_count": len(all_users)
        }

        put(f'portfolios/{id}/', payload)

        context.bot.send_message(chat_id,
                                 t("thanks", language))
