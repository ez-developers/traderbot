import logging
import dotenv
import os
from config.settings import AMOUNT_TO_PAY, CURRENCY
from bot.utils.language import lang
from bot.utils.request import get, post, put
from bot.src.text import t, b
from bot.src.menu import Menu
from telegram.ext import CallbackContext, ConversationHandler
from telegram import (Update,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      ReplyKeyboardMarkup,
                      ReplyKeyboardRemove,
                      KeyboardButton,
                      LabeledPrice)

dotenv.load_dotenv()


class Registration:
    """
    Base class for registration
    """

    def is_private_chat(self, chat_id: int):
        if chat_id > 0:
            return True
        else:
            return False

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name
        username = "@" + update.effective_user.username
        if self.is_private_chat(chat_id):
            all_users_id = []
            user_objects = get('users')
            for user in user_objects:
                all_users_id.append(user['id'])
            if chat_id in all_users_id:
                return self.check_data(update, context, chat_id)
            else:
                payload = {
                    "id": chat_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username
                }
                post('adduser/', payload)
                context.bot.send_message(chat_id,
                                         f"{t('greeting', lang='ru')}\n{t('greeting', lang='en')}",
                                         parse_mode='HTML')
                return self.request_language(update, context)
        else:
            return  # The bot is working in the group.

    def check_data(self, update, context, chat_id):
        user = get(f'users/{chat_id}')
        if user['subscription_status'] is False:
            return self.choose_subscription(update, context)
        else:
            return Menu().display(update, context)

    def request_language(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        markup = [
            [InlineKeyboardButton(b('language', lang='ru'), callback_data='ru'),
             InlineKeyboardButton(b('language', lang='en'), callback_data='en')]
        ]
        state = "LANGUAGE"

        context.bot.send_message(chat_id,
                                 f"{t('choose_language', lang='ru')}\n{t('choose_language', lang='en')}",
                                 reply_markup=InlineKeyboardMarkup(markup))

        logging.info(
            f'{chat_id} - choosing a language. Returned state: {state}')
        return state

    def get_language(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        query = update.callback_query
        query.answer()
        query.delete_message()

        if query.data == 'en':
            context.bot.send_message(chat_id,
                                     t("english_soon", lang="en"),
                                     parse_mode='HTML')
            return self.request_language(update, context)

        payload = {
            "id": chat_id,
            "language": query.data
        }
        put(f'users/{chat_id}/', payload)
        return self.accept_policy(update, context)

    def accept_policy(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "POLICY_AGREEMENT"
        context.bot.send_document(chat_id,
                                  document=open(
                                      'bot/assets/upload/document.pdf', 'rb'),
                                  caption=t('request_agreement',
                                            lang(chat_id)),
                                  reply_markup=InlineKeyboardMarkup([
                                      [InlineKeyboardButton(
                                          b('accept', lang(chat_id)), callback_data='accept'),
                                       InlineKeyboardButton(
                                          b('reject', lang(chat_id)), callback_data='reject')]
                                  ]),
                                  parse_mode='HTML')
        logging.info(
            f"{chat_id} - is given a document of privacy and policy for signature. Returned state: {state}")
        return state

    def handle_policy_accept(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        query = update.callback_query
        query.answer()
        query.delete_message()

        if query.data == 'accept':
            context.bot.send_document(chat_id,
                                      open('bot/assets/upload/document.pdf', 'rb'),
                                      caption=t('save_document', lang(chat_id)))
            return self.request_name(update, context)
        elif query.data == 'reject':
            context.bot.send_message(chat_id,
                                     t('policy_rejected', lang(chat_id)))
            return ConversationHandler.END

    def request_name(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "NAME"
        context.bot.send_message(chat_id,
                                 t("request_name", lang(chat_id)),
                                 reply_markup=ReplyKeyboardRemove())
        logging.info(
            f"{chat_id} - has accepted terms and conditions and now is being requested for his name. Returning state {state}")
        return state

    def get_name(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        name_input = update.effective_message.text
        full_name = name_input.split(" ")

        if len(full_name) == 2:
            payload = {
                "id": chat_id,
                "first_name": full_name[0],
                "last_name": full_name[1]
            }
        else:
            payload = {
                "id": chat_id,
                "first_name": name_input,
                "last_name": None
            }
        put(f"users/{chat_id}/", payload)
        context.bot.send_message(chat_id,
                                 t("name_accepted", lang(chat_id)))
        return self.request_phone(update, context)

    def request_phone(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "REQUESTING_PHONE"
        context.bot.send_message(chat_id=chat_id,
                                 text=t('request_phone', lang(chat_id)),
                                 reply_markup=ReplyKeyboardMarkup([
                                     [KeyboardButton(
                                         b('send_phone', lang(chat_id)), request_contact=True)],
                                 ], resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"{chat_id} is being requested his phone number. Returning state: {state}")
        return state

    def get_phone(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        message = update.effective_message

        if message.contact:
            phone = message.contact.phone_number
        else:
            phone = update.message.text
            if phone[:1] != '+':
                context.bot.send_message(chat_id,
                                         t("invalid_phone", lang(chat_id)))
        payload = {
            "id": chat_id,
            "phone_number": phone
        }
        put(f"users/{chat_id}/", payload)
        return self.choose_subscription(update, context)

    def choose_subscription(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "CHOOSING_SUBSCRIPTION"

        context.bot.send_message(chat_id,
                                 t('choose_subscription', lang(chat_id)),
                                 reply_markup=ReplyKeyboardMarkup([
                                     [KeyboardButton(
                                         b('subscribe', lang(chat_id)))],
                                     [KeyboardButton(
                                         b('enter_promocode', lang(chat_id)))]
                                 ], resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"{chat_id} - is choosing a subscription plan. Returning state: {state}")
        return state

    def subscribe(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = ConversationHandler.END

        title = "1 x course bundle"
        description = "This is your invoice for the subscription"
        payload = "I am paying for the course"
        provider_token = os.getenv('PAYMENT_TOKEN')
        currency = CURRENCY
        price = AMOUNT_TO_PAY
        prices = [LabeledPrice(b('pay', lang(chat_id)), price * 100)]

        context.bot.send_invoice(
            chat_id,
            title,
            description,
            payload,
            provider_token,
            currency,
            prices
        )

        logging.info(f"{chat_id} - paying. Returning state: {state}")
        return state

    def precheckout(self, update: Update, context: CallbackContext):
        query = update.pre_checkout_query
        if query.invoice_payload != 'I am paying for the course':
            query.answer(ok=False, error_message="Something went wrong...")
        else:
            query.answer(ok=True)

    def successful_payment(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        payload = {
            "id": chat_id,
            "subscription_status": True
        }
        put(f"users/{chat_id}/", payload)
        context.bot.send_message(chat_id, t('congratulations', lang(chat_id)))
        return Menu().display(update, context)

    def enter_promocode(self, update: Update, context: CallbackContext):
        update.effective_message.reply_text("Entering the promocode")