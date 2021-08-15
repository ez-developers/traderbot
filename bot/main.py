from bot.src import menu
from bot.src.text import b
import dotenv
import os
import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from bot.utils.filter import FilterButton
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
                    b["user_name"]), menu.username),
                MessageHandler(Filters.regex(
                    b["subscription_status"]), menu.subscription),
                MessageHandler(Filters.regex(
                    b["pay"]), menu.pay),
                MessageHandler(Filters.regex(
                    b["back"]), menu.display)
            ],
            "VIDEOS": [
                MessageHandler(Filters.regex(
                    b["back"]), menu.display),
                    MessageHandler(FilterButton("video_lessons"), menu.video_lessons)
            ]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(main_conversation)
    # dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
