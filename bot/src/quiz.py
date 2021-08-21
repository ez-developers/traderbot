from telegram.ext import CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from core.settings import GROUP_ID, USER_DETAILS_URL
from bot.src.menu import Menu
from bot.src.text import t, b
from bot.utils.language import lang
from bot.utils.request import get
from bot.utils.blocked import actions_blocked
import logging


class Quiz():

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        user = get(f'users/{chat_id}')
        language = user['language']
        state = "QUIZ"

        if user['subscription_status'] is False:
            actions_blocked(chat_id, language, context)
            return

        markup = [
            [KeyboardButton(b("start_quiz", language))],
            [KeyboardButton(b("back", language))]
        ]

        context.bot.send_message(chat_id,
                                 t("starting_quiz", language),
                                 reply_markup=ReplyKeyboardMarkup(
                                     markup, resize_keyboard=True),
                                 parse_mode='HTML')

        logging.info(
            f"{chat_id} - is about to start the quiz. Returned state: {state}")
        return state

    def save_response(self, update: Update, context: CallbackContext):
        response = update.message.text
        user_data = context.user_data['quiz']
        user_data[context.user_data['current_quiz']] = response

        payload = {
            "quiz": user_data
        }
        context.user_data.update(payload)

    def capital(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "CAPITAL"

        context.bot.send_message(chat_id,
                                 t("request_capital", language),
                                 reply_markup=ReplyKeyboardMarkup(
                                     [
                                         [KeyboardButton(b("back", language))]
                                     ], resize_keyboard=True),
                                 parse_mode='HTML')
        context.user_data.update(
            {
                "quiz": {},
                "current_quiz": state
            }
        )
        logging.info(
            f"{chat_id} - answering the first question. Returned state: {state}")
        return state

    def expectations(self, update: Update, context):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "EXPECTATIONS"
        self.save_response(update, context)

        context.bot.send_message(chat_id,
                                 t("request_expectations", language),
                                 reply_markup=ReplyKeyboardMarkup(
                                     [
                                         [KeyboardButton(b("back", language))]
                                     ], resize_keyboard=True),
                                 parse_mode='HTML')

        context.user_data.update(
            {
                "current_quiz": state
            }
        )
        logging.info(
            f"{chat_id} - answering the second question. Returned state: {state}")
        return state

    def risks(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "RISKS"
        buttons = [
            [KeyboardButton(b("yes", language)),
             KeyboardButton(b("no", language))],
            [KeyboardButton(b("back", language))]
        ]

        self.save_response(update, context)

        context.bot.send_message(chat_id,
                                 t("request_risk", language),
                                 reply_markup=ReplyKeyboardMarkup(
                                     buttons, resize_keyboard=True),
                                 parse_mode='HTML')

        context.user_data.update(
            {
                "current_quiz": state
            }
        )

        logging.info(
            f"{chat_id} - answering the third question. Returned state: {state}")
        return state

    def experience(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "EXPERIENCE"

        self.save_response(update, context)

        context.bot.send_message(chat_id,
                                 t('request_history', language),
                                 reply_markup=ReplyKeyboardMarkup(
                                     [
                                         [KeyboardButton(b("back", language))]
                                     ], resize_keyboard=True),
                                 parse_mode='HTML')

        context.user_data.update(
            {
                "current_quiz": state
            }
        )
        logging.info(
            f"{chat_id} - answering the fourth question. Returned state: {state}")
        return state

    def summary(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "SUMMARY"
        markup = [
            [
                KeyboardButton(b("back", language)),
                KeyboardButton(b("save_my_responses", language))
            ]
        ]
        answers = context.user_data['quiz']
        self.save_response(update, context)

        context.bot.send_message(chat_id,
                                 f"{t('accept_quiz', language)}"
                                 .format(
                                     t('request_capital', language),
                                     answers['CAPITAL'],
                                     t('request_expectations', language),
                                     answers['EXPECTATIONS'],
                                     t('request_risk', language),
                                     answers['RISKS'],
                                     t('request_history', language),
                                     answers['EXPERIENCE']
                                 ),
                                 reply_markup=ReplyKeyboardMarkup(
                                     markup, resize_keyboard=True),
                                 parse_mode='HTML')

        logging.info(
            f"{chat_id} - is viewing the summary of his responses. Returned state: {state}")
        return state

    def save_my_responses(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        user = get(f'users/{chat_id}')
        language = user['language']
        data = context.user_data['quiz']
        link_to_user = USER_DETAILS_URL + str(chat_id)
        response_to_group = f"""<b>Новый квиз!</b>

<i>Информация о пользователе:</i>
ID: <a href='{link_to_user}'>{chat_id}</a>
Имя: {user['first_name']}
Юзернейм: {user['username'] if user['username'] is not None else '-'}
Статус подписки: {'Активный' if user['subscription_status'] else 'Не активен'}

Ответы:
1. {t('request_capital', language)}:
<b>{data['CAPITAL']}</b>

2. {t('request_expectations', language)}
<b>{data['EXPECTATIONS']}</b>

3. {t('request_risk', language)}
<b>{data['RISKS']}</b>

4. {t('request_history', language)}
<b>{data['EXPERIENCE']}</b>
"""
        context.bot.send_message(GROUP_ID,
                                 response_to_group,
                                 parse_mode='HTML')

        context.bot.send_message(chat_id,
                                 t('response_saved', language),
                                 parse_mode='HTML')

        return Menu().display(update, context)
