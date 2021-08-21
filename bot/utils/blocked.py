from telegram import Update
from telegram.ext import CallbackContext
from bot.src.text import t, b


def actions_blocked(chat_id: int, language: str, context: CallbackContext):

    context.bot.send_message(chat_id,
                             f"{t('subscription_expired', language)}"
                             .format(
                                 b('extend_subscription', language),
                                 b('support', language)
                             ),
                             parse_mode='HTML')
