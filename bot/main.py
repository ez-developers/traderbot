from telegram.ext import (Updater,
                          CommandHandler,
                          ConversationHandler,
                          CallbackQueryHandler,
                          MessageHandler,
                          Filters,
                          PreCheckoutQueryHandler)
from core.settings import BOT_ID
from bot.src.registration import Registration
from bot.src.menu import Menu
from bot.src.profile import Profile
from bot.src.support import Support
from bot.src.group import Group
from bot.src.portfolio import Portfolio
from bot.src.video_lesson import VideoLesson
from bot.src.quiz import Quiz
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
video_lesson = VideoLesson()
quiz = Quiz()


def main():
    updater = Updater(token=os.getenv("BOT_TOKEN"))
    dispatcher = updater.dispatcher

    quiz_conversation = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(buttons('quiz')), quiz.start)
        ],
        states={
            "QUIZ": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(Filters.regex(
                    buttons('start_quiz')), quiz.capital)
            ],
            "CAPITAL": [
                MessageHandler(Filters.regex(buttons('back')), quiz.start),
                MessageHandler(Filters.text, quiz.expectations)
            ],
            "EXPECTATIONS": [
                MessageHandler(Filters.regex(buttons('back')), quiz.capital),
                MessageHandler(Filters.text, quiz.risks)
            ],
            "RISKS": [
                MessageHandler(Filters.regex(
                    buttons('back')), quiz.expectations),
                MessageHandler(Filters.regex(buttons('yes')) |
                               Filters.regex(buttons('no')), quiz.experience)
            ],
            "EXPERIENCE": [
                MessageHandler(Filters.regex(
                    buttons('back')), quiz.risks),
                MessageHandler(Filters.text, quiz.summary)
            ],
            "SUMMARY": [
                MessageHandler(Filters.regex(
                    buttons('back')), quiz.experience),
                MessageHandler(Filters.regex(
                    buttons('save_my_responses')), quiz.save_my_responses)
            ]
        },
        fallbacks=[],
        map_to_parent={
            "MENU_DISPLAYED": "MENU_DISPLAYED"
        }
    )

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', registration.start)],
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
                ConversationHandler(
                    entry_points=[
                        MessageHandler(Filters.regex(
                            buttons('subscribe')), registration.subscribe),
                    ],
                    states={
                        "INITIAL_PAYING": [
                            MessageHandler(Filters.regex(buttons('cancel_pay')),
                                           registration.cancel_pay),
                            PreCheckoutQueryHandler(registration.precheckout),
                            MessageHandler(Filters.successful_payment,
                                           registration.successful_payment),
                        ]
                    },
                    fallbacks=[],
                    map_to_parent={
                        "CHOOSING_SUBSCRIPTION": "CHOOSING_SUBSCRIPTION",
                        "MENU_DISPLAYED": "MENU_DISPLAYED"
                    },
                    per_chat=False
                ),
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
                MessageHandler(Filters.regex(buttons('videos')),
                               menu.video_lessons),
                MessageHandler(Filters.regex(
                    buttons('support')), menu.support),
                quiz_conversation
            ],
            "MY_PROFILE": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(Filters.regex(
                    buttons('my_info')), profile.my_info),
                MessageHandler(Filters.regex(
                    buttons('subscription_status')), profile.subscription_status),
                MessageHandler(Filters.regex(
                    buttons('extend_subscription')), profile.choose_plan)
            ],
            "CHOOSING_PLANS": [
                MessageHandler(Filters.regex(
                    buttons('back')), menu.my_profile),

                ConversationHandler(
                    entry_points=[
                        MessageHandler(
                            Filters.regex(buttons('1_year')) |
                            Filters.regex(buttons('3_years')) |
                            Filters.regex(buttons('5_years')), profile.extend_subscription)
                    ],
                    states={
                        "EXTENDING_PAY": [
                            MessageHandler(Filters.regex(
                                buttons('cancel_pay')), profile.cancel_extending),
                            PreCheckoutQueryHandler(profile.precheckout),
                            MessageHandler(Filters.successful_payment,
                                           profile.successful_payment)
                        ]
                    },
                    fallbacks=[],
                    per_chat=False,
                    map_to_parent={
                        "CHOOSING_PLANS": "CHOOSING_PLANS",
                        "MENU_DISPLAYED": "MENU_DISPLAYED"
                    }
                )
            ],
            "PORTFOLIOS": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(FilterButton('portfolios'),
                               portfolio.handle_portfolio_click)
            ],
            "SUPPORT": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(Filters.all, support.accept)
            ],
            "VIDEOS": [
                MessageHandler(Filters.regex(buttons('back')), menu.display),
                MessageHandler(FilterButton('videos'),
                               video_lesson.display)
            ]
        },
        fallbacks=[
            CommandHandler('start', registration.start),
            CommandHandler('pay', profile.choose_plan),
            CommandHandler('support', menu.support)
        ],
        per_chat=False
    )

    dispatcher.add_handler(main_conversation)
    dispatcher.add_error_handler(error_handler)
    dispatcher.add_handler(MessageHandler(
        ReplyToMessageFilter(Filters.user(BOT_ID)), group.reply_to_user))

    updater.start_polling()
    updater.idle()
