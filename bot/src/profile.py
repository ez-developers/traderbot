from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice
from core.settings import (CURRENCY,
                           AMOUNT_TO_PAY,
                           INVOICE_TITLE,
                           INVOICE_DESCRIPTION)
from bot.src.menu import Menu
from bot.src.text import t, b
from bot.utils.request import get, put
from bot.utils.language import lang
import datetime
import locale
import logging
import os
import dotenv

dotenv.load_dotenv()


class Profile():

    def my_info(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        user = get(f"users/{chat_id}")

        context.bot.send_message(chat_id,
                                 f"{t('my_info', language)}"
                                 .format(
                                     user['id'],
                                     user['first_name'],
                                     user['last_name'] if user['last_name'] is not None else "-",
                                     user['phone_number']
                                 ), parse_mode='HTML')

    def subscription_status(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        user = get(f'users/{chat_id}')
        language = user['language']
        status = user['subscription_status']
        locale.setlocale(
            locale.LC_ALL, f'{language}_{language.upper()}.utf-8')
        date = datetime.datetime.strptime(
            user['subscribed_until'], "%Y-%m-%d").strftime('%d %B %Y')

        if status == True:
            context.bot.send_message(chat_id,
                                     f'{t("subscription_status", language)}: <b>{t("active", language)}</b>\n{t("expiry_date", language)}: <b>{date}</b>', parse_mode='HTML')
        else:
            context.bot.send_message(chat_id,
                                     f'{t("subscription_status", language)}: <b>{t("not_active", language)}</b>', parse_mode='HTML')

    def choose_plan(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        markup = [
            [
                KeyboardButton(b('1_year', language)),
                KeyboardButton(b('3_years', language)),
                KeyboardButton(b('5_years', language)),
            ],
            [KeyboardButton(b('back', language))]
        ]
        state = "CHOOSING_PLANS"

        context.bot.send_message(chat_id,
                                 t('choosing_plans', language),
                                 reply_markup=ReplyKeyboardMarkup(markup,
                                                                  resize_keyboard=True),
                                 parse_mode='HTML')

        logging.info(
            f"{chat_id} - is extending his subscription. Returned state: {state}")
        return state

    def extend_subscription(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        years = update.effective_message.text[0]
        state = "EXTENDING_PAY"

        invoice_payload = "I am extending the subscription"
        provider_token = os.getenv('PAYMENT_TOKEN')
        currency = CURRENCY
        price = AMOUNT_TO_PAY * int(years)
        prices = [LabeledPrice(b('pay', language), price * 100)]

        context.bot.send_message(chat_id,
                                 t('pay_the_cheque', language),
                                 reply_markup=ReplyKeyboardMarkup([
                                     [KeyboardButton(
                                         b('cancel_pay', language))]
                                 ], resize_keyboard=True),
                                 parse_mode='HTML')

        invoice = context.bot.send_invoice(
            chat_id,
            INVOICE_TITLE,
            INVOICE_DESCRIPTION,
            invoice_payload,
            provider_token,
            currency,
            prices
        )

        user_payload = {
            "invoice_id": invoice.message_id,
            "years_paid": int(years)
        }
        context.user_data.update(user_payload)

        logging.info(
            f"{chat_id} - extending his subscription. Returning state: {state}")
        return state

    def precheckout(self, update: Update, context: CallbackContext):
        query = update.pre_checkout_query
        if query.invoice_payload != 'I am extending the subscription':
            query.answer(
                ok=False, error_message="Что-то пошло не так. Свяжитесь с администраторами...")
        else:
            query.answer(ok=True)

    def successful_payment(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        user = get(f'users/{chat_id}')
        language = user['language']
        locale.setlocale(
            locale.LC_ALL, f'{language}_{language.upper()}.utf-8')
        years_paid = context.user_data['years_paid']
        year = 365
        subscribed_until = datetime.datetime.strptime(
            user['subscribed_until'], '%Y-%m-%d')
        subscribscription_extend = datetime.timedelta(days=year*years_paid)
        now = datetime.datetime.now()

        if subscribed_until < now:
            extended_till = now + subscribscription_extend
        else:
            extended_till = subscribed_until + subscribscription_extend

        user_display_date = datetime.datetime.strftime(
            extended_till, "%d %B %Y")

        payload = {
            "id": chat_id,
            "subscription_status": True,
            "subscribed_until": f"{extended_till.date()}",
            "number_of_subscriptions": user['number_of_subscriptions'] + 1
        }

        put(f"users/{chat_id}/", payload)

        invoice_id = context.user_data['invoice_id']
        context.bot.delete_message(chat_id,
                                   message_id=invoice_id)
        context.bot.send_message(chat_id,
                                 f"{t('subscription_extended', language)}"
                                 .format(user_display_date),
                                 parse_mode='HTML')
        return Menu().display(update, context)

    def cancel_extending(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        context.bot.delete_message(chat_id,
                                   message_id=context.user_data['invoice_id'])

        return self.choose_plan(update, context)
