from telegram import Update, chat
from telegram.ext import CallbackContext
from bot.src.text import t
from bot.src.menu import Menu
from bot.utils.request import get, put, get_target_id_by_name
from bot.utils.language import lang


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
            all_users.remove(chat_id)
            context.bot.send_message(chat_id,
                                     t('unfollowed', language),
                                     parse_mode='HTML')
        else:
            all_users.append(chat_id)
            context.bot.send_message(chat_id,
                                     t("followed", language),
                                     parse_mode='HTML')

        payload = {
            "users_list": all_users,
            "users_count": len(all_users)
        }

        put(f'portfolios/{id}/', payload)
        return Menu().portfolio(update, context)
