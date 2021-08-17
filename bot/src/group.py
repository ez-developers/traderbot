from telegram.ext import CallbackContext
from telegram import Update
from config.settings import GROUP_ID
from bot.src.text import t
from bot.utils.language import lang


class Group:

    def reply_to_user(self, update: Update, context: CallbackContext):
        try:
            if update.message.reply_to_message:

                response = update.message.text

                reply_id = update.message.reply_to_message.message_id

                user_id = context.bot_data[reply_id]

                language = lang(user_id)

                reply = t("reply_to_user", language)

                context.bot.send_message(chat_id=user_id,
                                         text=f"{reply}".format(response),
                                         parse_mode='HTML')
                update.effective_message.reply_text(
                    "Отлично! Я отправил ваш ответ пользователю.")
            else:
                pass
        except KeyError:
            update.effective_message.reply_text(
                "Ошибка на сервере! Попробуйте ответить на более недавние сообщения")
