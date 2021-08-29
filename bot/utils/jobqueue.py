# TODO: If user's subscription is already inactive, then remove him (chat_id
# from all portfolios and his subscriptions. Completely disable his account, so that he won't get updates from trader-admin.)
from telegram import Update
from telegram.ext import CallbackContext
from core.settings import TIME_ZONE
from bot.src.text import t, b
from bot.utils.request import get, put, get_target_id_by_name
import datetime
import pytz


def run_job(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.job_queue.run_daily(
        handle_subscription, time=datetime.time(hour=0, minute=0, second=0, tzinfo=pytz.timezone(TIME_ZONE)), context=chat_id, name=str(chat_id))


def handle_subscription(context: CallbackContext):
    job = context.job
    chat_id = job.context
    user = get(f'users/{chat_id}')
    language = user['language']
    portfolios = get('portfolios')
    subscription_status = user['subscription_status']

    # If the user has just started the bot as a new user and job queue
    # started a job, it will not check him for subscription expiration date.
    # That's because new user's subscribed_until returns None.
    if user['subscribed_until'] is not None:
        subscription_expiration = datetime.datetime.strptime(
            user['subscribed_until'], '%Y-%m-%d')
    else:
        return
    today = datetime.datetime.now()

    if subscription_expiration < today and subscription_status is True:
        user_payload = {
            "id": chat_id,
            "subscription_status": False
        }

        for portfolio in portfolios:
            all_users = []
            current = portfolio['name']
            id = get_target_id_by_name('portfolios', current)

            for i in portfolio['users_list']:
                all_users.append(i)

            if chat_id in all_users:

                all_users.remove(chat_id)

                portfolios_payload = {
                    "users_list": all_users,
                    "users_count": len(all_users)
                }
                put(f'portfolios/{id}/', portfolios_payload)
            else:
                continue

        put(f'users/{chat_id}/', user_payload)
        context.bot.send_message(chat_id,
                                 f"{t('expiration_notification', language)}"
                                 .format(
                                     b('my_profile', language),
                                     b('extend_subscription', language)
                                 ),
                                 parse_mode='HTML')
