import html
import json
import logging
import traceback

from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from config.settings import ADMIN_IDS


class ButtonError(Exception):
    pass


def error_handler(update: object, context: CallbackContext) -> None:
    logging.error(msg="Exception while handling an update:",
                  exc_info=context.error)
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )
    for admin in ADMIN_IDS:
        context.bot.send_message(chat_id=admin,
                                 text=message, parse_mode=ParseMode.HTML)
