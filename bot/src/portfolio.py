from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.request import get, put, get_target_id_by_name
from bot.utils.language import lang
from bot.src.text import t


class Portfolio():

    def handle_portfolio_click(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        id = get_target_id_by_name('portfolios', update.message.text)

        portfolio = get(f'portfolios/{id}')

        if chat_id in portfolio['user_list']:
            update.edited_message.reply_text("you have already chosen it")
        else:
            updated_users = portfolio['user_list'].append(chat_id)
            payload = {
                "user_list": updated_users,
                "user_count": len(updated_users)
            }

            put(f'portfolios/{id}/', payload)

            context.bot.send_message(chat_id,
                                     t("thanks", language))
