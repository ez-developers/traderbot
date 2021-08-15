from bot.src import menu
from bot.src.text import b
import dotenv
import os
import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, filters
from bot.utils.filter import FilterButton, buttons
from bot.src.registration import Registration
from bot.src.error import error_handler

dotenv.load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

registration = Registration()


def main():
    updater = Updater(token=os.getenv("BOT_TOKEN"))
    dispatcher = updater.dispatcher

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', registration.start)
        ],
        states={
            "LANGUAGE": [
                
            ],
            "MENU_DISPLAYED": [

            ],
            "MY_PROFILE": [
                MessageHandler(Filters.regex(
                    buttons("user_name")), menu.username),
                MessageHandler(Filters.regex(
                    buttons("subscription_status")), menu.subscription),
                MessageHandler(Filters.regex(
                    buttons("pay")), menu.pay),
                MessageHandler(Filters.regex(
                    buttons("back")), menu.display)
            ],
            "VIDEOS": [
                MessageHandler(FilterButton(
                    buttons("video_lessons")), menu.video_lessons),
                MessageHandler(Filters.regex(
                    buttons("back")), menu.display)
            ],
            "SUPPORT": [
                MessageHandler(Filters.text|
                                Filters.audio|
                                Filters.video|
                                Filters.photo, menu.support),
                MessageHandler(Filters.regex(
                    buttons("back")), menu.display)             
            ]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(main_conversation)
    # dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
