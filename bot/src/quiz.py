from bot.utils.language import lang
from bot.src.text import t, b
from telegram.ext import CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, chat
import logging




class Quiz():
    
    def question1(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "QUIZ"
        back = [KeyboardButton(b("back", language))]
        context.bot.send_message(chat_id,
                                 t("request_capital", language),
                                 reply_markup = ReplyKeyboardMarkup(
                                     [back], resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"{chat_id} - answering first question. Returned state: {self.question2}")
        return self.question2
    
    def question2(self, update: Update, context):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "QUIZ"
        back = [KeyboardButton(b("back", language))]
        context.bot.send_message(chat_id,
                                 t("request_expectations", language),
                                 reply_markup = ReplyKeyboardMarkup(back, resize_keyboard=True),
                                 parse_mode='HTML')
        
        logging.info(
            f"{chat_id} - answering second question. Returned state: {state}")
        return self.question3
    
    def question3(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "QUIZ"
        buttons = [
            [KeyboardButton(b("yes", language)),
            KeyboardButton(b("no", language))]
            [KeyboardButton(b("back", language))]]
        
        context.bot.send_message(chat_id,
                                 t("request_risk", language),
                                 reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')
        
        logging.info(
            f"{chat_id} - answering third question. Returned state: {state}")
        return state
        
    
    def question4(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "QUIZ"
        back = [
            [KeyboardButton(b("back", language))]
        ]
        
        context.bot.send_message(chat_id,
                                 t('request_history', language),
                                 reply_markup = ReplyKeyboardMarkup(back, resize_keyboard=True),
                                 parse_mode='HTML')
        logging.info(
            f"{chat_id} - answering fourth question. Returned state: {state}")
        return Quiz().accept
    
    def accept(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        language = lang(chat_id)
        state = "QUIZ"
        finish = [
            [KeyboardButton(b("finish", language))]
        ]
        
        context.bot.send_message(chat_id,
                                 t('accept_quiz', language),
                                 reply_markup = ReplyKeyboardMarkup(finish, resize_keyboard=True),
                                 parse_mode='HTML')
        
        logging.info(
            f"{chat_id} - finishing questionaire. Returned state: {state}")
        return state