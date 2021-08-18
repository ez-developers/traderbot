from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.request import get, put, get_target_id_by_name
from bot.utils.language import lang
from bot.src.text import t
import json


class Portfolio():

    def handle_portfolio_click(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        id = get_target_id_by_name('portfolios', update.message.text)

        portfolio = get(f'portfolios/{id}')
        users = []
        for i in portfolio['user_list']:
            users.append(i)
        print(users)

        # TODO: Very huge bug here. Please, help with this, guys!
        updated_users = ['sdfsd', 'sd'].append(str(chat_id))
        print(updated_users)
        payload = {
            "user_list": updated_users,
            "user_count": portfolio['user_count'] + 1
        }

        put(f'portfolios/{id}/', payload)

        context.bot.send_message(chat_id,
                                 t("thanks", language))
