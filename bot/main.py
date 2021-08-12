import dotenv
import os
import logging
from telegram.ext import Updater, CommandHandler
from bot.src.error import error_handler

dotenv.load_dotenv()


def test(update, context):
    print("Worked!")


def main():
    updater = Updater(token=os.getenv("BOT_TOKEN"))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', test))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
