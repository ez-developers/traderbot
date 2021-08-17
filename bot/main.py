from telegram.ext import (Updater,
                          CommandHandler,
                          ConversationHandler,
                          CallbackQueryHandler,
                          MessageHandler,
                          Filters,
                          PreCheckoutQueryHandler)
from config.settings import BOT_ID
from bot.src.registration import Registration
from bot.src.menu import Menu
from bot.src.profile import Profile
from bot.src.support import Support
from bot.src.group import Group
from bot.src.portfolio import Portfolio
from bot.src.error import error_handler
from bot.utils.filter import buttons, FilterButton
from bot.utils.reply_to_message_filter import ReplyToMessageFilter
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
profile = Profile()
support = Support()
group = Group()
portfolio = Portfolio()


def main():
    updater = Updater(token=os.getenv("BOT_TOKEN"))
    dispatcher = updater.dispatcher

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', registration.start),
            MessageHandler(Filters.successful_payment,
                           registration.successful_payment),
            MessageHandler(Filters.regex(buttons('cancel_pay')),
                           registration.cancel_pay)
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
                    buttons('back')), menu.my_profile),
                MessageHandler(Filters.regex(
                    buttons('subscribe')), registration.subscribe),
                MessageHandler(Filters.regex(
                    buttons("enter_promocode")), registration.enter_promocode)
            ],
            "PROMOCODE": [
                MessageHandler(Filters.regex(buttons('back')),
                               registration.choose_subscription),
                MessageHandler(Filters.text, registration.validate_promocode)
            ],
            "MENU_DISPLAYED": [
                MessageHandler(Filters.regex(
                    buttons('my_profile')), menu.my_profile),
                MessageHandler(Filters.regex(
                    buttons('portfolio')), menu.portfolio),
                MessageHandler(Filters.regex(buttons('support')), menu.support)
            ],
            "MY_PROFILE": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(Filters.regex(
                    buttons('my_info')), profile.my_info),
                MessageHandler(Filters.regex(
                    buttons('subscription_status')), profile.subscription_status),
                MessageHandler(Filters.regex(
                    buttons('extend_subscription')), profile.extend_subscription)
            ],
            "PORTFOLIOS": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(FilterButton('portfolios'),
                               portfolio.handle_portfolio_click)
            ],
            "SUPPORT": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(Filters.text, support.accept)
            ],
            "VIDEOS": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(FilterButton('videos'), menu.display)
            ]
        },
        fallbacks=[
            CommandHandler('start', registration.start)
        ]
    )

    dispatcher.add_handler(main_conversation)
    dispatcher.add_handler(PreCheckoutQueryHandler(registration.precheckout))
    # dispatcher.add_error_handler(error_handler)
    dispatcher.add_handler(MessageHandler(
        ReplyToMessageFilter(Filters.user(BOT_ID)), group.reply_to_user))

    updater.start_polling()
    updater.idle()
