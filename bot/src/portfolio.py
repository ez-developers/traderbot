from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.request import get, put
from bot.utils.language import lang


class Portfolio():

    def handle_portfolio_click(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        target_portfolio = update.message.text
        language = lang(chat_id)
        all_portfolios = get('portfolios')

        for i in all_portfolios:
            if i['name'] == target_portfolio:
                this_portfolio_id = i['id']

        user_choice = get(f'portfolios/{this_portfolio_id}')

        if chat_id in user_choice['user_list']:
            update.edited_message.reply_text("you have already chosen it")
        else:
            updated_users = user_choice['user_list'].append(chat_id)
            payload = {
                "user_list": updated_users,
                "user_count": len(updated_users)
            }

            put(f'portfolios/{this_portfolio_id}/', payload)

            context.bot.send_message(chat_id,
                                     "you clicked successfully")
