from telegram.ext import CallbackContext
from telegram import Update
from core.settings import GROUP_ID
from bot.src.text import t
from bot.utils.language import lang


class Group:

    def reply_to_user(self, update: Update, context: CallbackContext):
        if not update.message.reply_to_message.forward_date:
            update.effective_message.reply_text(
                "❗️ Ответы возможны только для <b>пересланных сообщений</b> от бота (Forwarded from: ...)", parse_mode='HTML')
            return

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

        except KeyError:
            update.effective_message.reply_text(
                "Попробуйте ответить на более недавние сообщения.")
