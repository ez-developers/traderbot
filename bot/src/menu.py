from telegram import (ReplyKeyboardMarkup,
                      Update,
                      KeyboardButton,
                      ChatAction,
                      InputMediaPhoto,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import CallbackContext
from bot.src.text import t, b
from bot.utils.build_menu import build_menu
from bot.utils.request import (parser,
                               target_category_id,
                               products_list,
                               product_det,
                               notification_on,
                               get)
from config.settings import API_URL, API_AUTHENTICATION, BASE_DIR, GROUP_ID
import logging
import time
import json
import requests

j = json.load(open("bot/assets/text.json", "r"))
text = j["texts"]
button = j["buttons"]
menu_button = j["buttons"]


class Menu:
    def __init__(self):
        self.menu_buttons = [
            [KeyboardButton(b("my_profile")),
             KeyboardButton(b("video_lessons"))],
            [KeyboardButton(b("support")),
             KeyboardButton(b("portfolios"))]
        ]

    def display(self, update: Update, context: CallbackContext):
        state = "MENU_DISPLAYED"
        chat_id = update.effective_chat.id

        context.bot.send_message(chat_id,
                                 t("main_page"),
                                 reply_markup=ReplyKeyboardMarkup(
                                     self.menu_buttons, resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"{chat_id} - opened main menu. Returned state: {state}")
        return state

    def categories(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "CATEGORIES"
        buttons = parser(API_URL=API_URL + "categories/",
                         API_auth=API_AUTHENTICATION,
                         key='name')

        context.bot.send_message(chat_id,
                                 f'{text["category"]}',
                                 reply_markup=ReplyKeyboardMarkup(
                                     build_menu(
                                         buttons=[KeyboardButton(
                                             s) for s in buttons],
                                         n_cols=2,
                                         footer_buttons=[
                                             KeyboardButton(
                                                 menu_button["back"])]
                                     ), resize_keyboard=True
                                 ),
                                 parse_mode='HTML')
        logging.info(
            f"User {chat_id} opened categories. Returned state: {state}")
        return state

    def products(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        target_id = target_category_id(update.message.text)
        state = "PRODUCTS"
        buttons = products_list(target_id)

        context.bot.send_message(chat_id,
                                 f'{text["product"]}',
                                 reply_markup=ReplyKeyboardMarkup(
                                     build_menu(
                                         buttons=[KeyboardButton(
                                             s) for s in buttons],
                                         n_cols=1,
                                         footer_buttons=[
                                             KeyboardButton(
                                                 menu_button["back"])]

                                     ), resize_keyboard=True
                                 ),
                                 parse_mode='HTML')
        logging.info(
            f"User {chat_id} opened products. Returned state: {state}")
        return state

    def product_details(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        requested_product = update.message.text
        product = product_det(requested_product)
        product_images = []
        price = str(product['price'])
        formatted_price = ' '.join([price[::-1][i:i+3]
                                   for i in range(0, len(price), 3)])[::-1]
        caption = f"""<b>{product['name']}</b>

<b>Тавсиф:</b>
{product['description']}

<b>Нархи:</b>
$ {formatted_price}"""
        like_button = [
            InlineKeyboardButton(button['like_it'], callback_data='like')
        ]

        for i in range(1, 11):
            product_images.append(product[f'image_{i}'])
        displayed = []
        for image in product_images:
            if image is not None:
                displayed.append(str(BASE_DIR) + image)

        # context.bot.send_message(chat_id, text['downloading'])
        context.bot.send_chat_action(chat_id,
                                     action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_media_group(chat_id,
                                     media=[
                                         InputMediaPhoto(media=open(j, 'rb')) for j in displayed
                                     ])
        time.sleep(1)
        context.bot.send_message(chat_id, caption,
                                 parse_mode='HTML',
                                 reply_markup=InlineKeyboardMarkup([
                                     like_button
                                 ]))

    def product_like(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        query = update.callback_query
        user = get(f"users/{chat_id}")
        query.answer()
        update.effective_message.reply_text(
            "Сизга маҳсулотимиз ёққанидан мамнунмиз 😊")
        context.bot.send_message(GROUP_ID,
                                 f"""<b>{user['name']}</b>га қуйидаги маҳсулот ёқди 👇""",
                                 parse_mode='HTML')
        query.copy_message(GROUP_ID)

    def settings(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "SETTINGS"
        notif_status = notification_on(chat_id)
        notifcation_button = button["notification_off"] if notif_status else button["notification_on"]

        buttons = [
            [button["change_phone"],
             button["change_name"]],
            [notifcation_button],
            [menu_button['back']]
        ]
        context.bot.send_message(chat_id,
                                 text["settings"],
                                 reply_markup=ReplyKeyboardMarkup(
                                     buttons, resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"User {chat_id} opened settings. Returned state: {state}")
        return state

    def change_notification_status(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        user = get(f'users/{chat_id}')
        if notification_on(chat_id):
            user['notifications'] = False
            update.effective_message.reply_text(
                "Сиз билдиришномаларни бекор қилдингиз!")
        else:
            user['notifications'] = True
            update.effective_message.reply_text(
                "Билдиришномаларга обуна янгиланди!")
        requests.put(API_URL + f'users/{chat_id}',
                     auth=API_AUTHENTICATION,
                     json=user,
                     headers={'Content-Type': 'application/json'})
        logging.info(
            f"User {chat_id} has changed his notification preferences to {user['notifications']}")
        return self.settings(update, context)

    def change_name(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        state = "EDITING_NAME"
        context.bot.send_message(chat_id,
                                 text["enter_name"],
                                 reply_markup=ReplyKeyboardMarkup([
                                     [menu_button["back"]]
                                 ], resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"User {chat_id} is changing name. Returned state: {state}")
        return state

    def get_name(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        name = update.effective_message.text

        user = get(f'users/{chat_id}')
        user['name'] = name
        requests.put(API_URL + f"users/{chat_id}",
                     auth=API_AUTHENTICATION,
                     json=user)
        update.effective_message.reply_text(
            "<b>Тайёр! ✅</b>", parse_mode='HTML')
        return self.settings(update, context)
