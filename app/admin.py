from django.contrib import admin, messages
from core.settings import DJANGO_DEVELOPER_ID, BASE_DIR
from .models import User, Promo, Portfolio, VideoLesson, BroadcastSelective, BroadcastAll
from .forms import CustomActionForm
import time
import os
import dotenv
import telegram
from telegram.error import Unauthorized

dotenv.load_dotenv()

bot = telegram.Bot(os.getenv("BOT_TOKEN"))

admin.site.site_url = None
admin.site.index_title = "Добро пожаловать!"
admin.site.site_title = "Администрация «Trader One™"
admin.site.site_header = "Администрация Trader One™"


@ admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username",
                    "phone_number", "subscription_status", "date_joined", "subscribed_until")
    exclude = ("number_of_subscriptions",)
    list_display_links = ("id",)
    list_filter = ("subscribed_until", ('subscription_status',
                                        admin.BooleanFieldListFilter),)
    search_fields = ("first_name", )
    list_per_page = 50

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@ admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ("promo_id", "valid_date", "is_active")
    readonly_fields = ("promo_id", "is_active")
    list_per_page = 50
    action_form = CustomActionForm

    def has_delete_permission(self, request, obj=None):
        return False


@ admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("name", "users_count")
    readonly_fields = ("users_count",)
    exclude = ("users_list",)
    actions_selection_counter = True
    action_form = CustomActionForm
    list_per_page = 50


@ admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_per_page = 50
    action_form = CustomActionForm


@admin.register(BroadcastSelective)
class BroadcastSelectiveAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_add(self, request, obj):
        msg = "Сообщения успешно отправлены пользователям"
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)

    def response_post_save_add(self, request, obj):

        image = request.FILES.get('image')
        message = request.POST.get('message')
        portfolio = request.POST.get('portfolio')
        all_users = list(Portfolio.objects.filter(pk=portfolio)
                         .values('users_list')[0]['users_list'])

        if image is not None:
            image_path = open(
                str(BASE_DIR)
                + f'/uploads/broadcast-selective/{time.strftime("%Y_%m_%d")}/{image}', "rb")

            for i in all_users:
                try:
                    response = bot.send_photo(i,
                                              image_path,
                                              caption=message)
                    photo_id = response.photo[-1]['file_id']
                    all_users = all_users[all_users.index(i) + 1:]
                    break
                except Unauthorized:
                    all_users = all_users[all_users.index(i) + 1:]
                    continue

            for user in all_users:
                try:
                    bot.send_photo(user,
                                   photo_id,
                                   caption=message,
                                   parse_mode='HTML')
                    time.sleep(0.03)
                except Unauthorized:
                    continue
        else:

            for user in all_users:
                try:
                    bot.send_message(user, message, parse_mode='HTML')
                    time.sleep(0.03)
                except Unauthorized:
                    continue

        return super(BroadcastSelectiveAdmin, self).response_post_save_add(request, obj)

    list_display = ("message", "date_sent", "portfolio")
    list_per_page = 50
    action_form = CustomActionForm


@admin.register(BroadcastAll)
class BroadcastAllAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_add(self, request, obj):
        msg = "Сообщения успешно отправлены пользователям"
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)

    def response_post_save_add(self, request, obj):
        image = request.FILES.get('image')
        message = request.POST.get('message')
        all_users = list(User.objects.values_list("id"))
        # Returns a list of tuples. Each tuple is one chat_id.
        # Example: [(44211,), (1231321231,), (342452,), (3424,)]

        if image is not None:
            image_path = open(
                str(BASE_DIR)
                + f'/uploads/broadcast-all/{time.strftime("%Y_%m_%d")}/{image}', "rb")

            for i in all_users:
                try:
                    response = bot.send_photo(i[0],
                                              image_path,
                                              caption=message)
                    photo_id = response.photo[-1]['file_id']
                    all_users = all_users[all_users.index(i) + 1:]
                    break
                except Unauthorized:
                    all_users = all_users[all_users.index(i) + 1:]
                    continue

            for user in all_users:
                try:
                    bot.send_photo(user[0],
                                   photo_id,
                                   caption=message,
                                   parse_mode='HTML')
                    time.sleep(0.03)
                except Unauthorized:
                    continue

        else:

            for user in all_users:
                try:
                    bot.send_message(user[0], message, parse_mode='HTML')
                    time.sleep(0.03)
                except Unauthorized:
                    continue

        return super(BroadcastAllAdmin, self).response_post_save_add(request, obj)

    action_form = CustomActionForm
