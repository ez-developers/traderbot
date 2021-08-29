from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.language import lang
from bot.utils.request import get, get_target_id_by_name


class VideoLesson():

    def display(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        id = get_target_id_by_name('videos', update.message.text)
        video = get(f'videos/{id}')

        context.bot.send_message(chat_id,
                                 f"{video['url']}")
