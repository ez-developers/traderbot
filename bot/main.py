from telegram.ext import (Updater,
                          CommandHandler,
                          ConversationHandler,
                          CallbackQueryHandler,
                          MessageHandler,
                          Filters,
                          PreCheckoutQueryHandler, ShippingQueryHandler)
from bot.src.registration import Registration
from bot.src.menu import Menu
from bot.src.error import error_handler
from bot.utils.filter import buttons
import dotenv
import os
import logging

dotenv.load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

registration = Registration()
menu = Menu()


def main():
    updater = Updater(token=os.getenv("BOT_TOKEN"))
    dispatcher = updater.dispatcher

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', registration.start),
            MessageHandler(Filters.successful_payment,
                           registration.successful_payment)
        ],
        states={
            "LANGUAGE": [
                CallbackQueryHandler(
                    registration.get_language, pattern='ru|en')
            ],
            "POLICY_AGREEMENT": [
                CallbackQueryHandler(
                    registration.handle_policy_accept, pattern='accept|reject')
            ],
            "NAME": [
                MessageHandler(Filters.text, registration.get_name)
            ],
            "REQUESTING_PHONE": [
                MessageHandler(Filters.text | Filters.contact,
                               registration.get_phone)
            ],
            "CHOOSING_SUBSCRIPTION": [
                MessageHandler(Filters.regex(
                    buttons('subscribe')), registration.subscribe),
                MessageHandler(Filters.regex(
                    buttons("enter_promocode")), registration.enter_promocode)
            ],
            "MENU_DISPLAYED": [

            ],
            "MY_PROFILE": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(Filters.regex(buttons('user_name')), menu.my_info),
                MessageHandler(Filters.regex(buttons('subscription_status')), menu.subscription_status),
                MessageHandler(Filters.regex(buttons('pay')), registration.choose_subscription)
            ]
        },
        fallbacks=[
            CommandHandler('start', registration.start)
        ]
    )

    dispatcher.add_handler(main_conversation)
    dispatcher.add_handler(PreCheckoutQueryHandler(registration.precheckout))
    # dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
