from django.contrib import admin
from django.http import HttpResponseRedirect
from core.settings import DJANGO_DEVELOPER_ID, BASE_DIR
from .models import User, Promo, Portfolio, VideoLesson, Mailings
from .forms import CustomActionForm
import time
import os
import dotenv
import telebot

dotenv.load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

admin.site.site_url = None
admin.site.index_title = "Добро пожаловать!"
admin.site.site_title = "Администрация «Trader One™"
admin.site.site_header = "Администрация Trader One™"


@admin.register(Mailings)
class MailingsAdmin(admin.ModelAdmin):

    def response_post_save_add(self, request, obj):

        image = request.FILES.get('image', None)
        message = request.POST.get('message', None)

        if not image:

            for el in User.objects.values_list('id',):
                try:
                    bot.send_message(el[0], message, parse_mode='HTML')
                except Exception as e:
                    print("ID неправылный или бота заблокировал")
        else:

            path = open(
                str(str(BASE_DIR) + f'/uploads/images/{str(image)}'), "rb")

            photo = bot.send_photo((DJANGO_DEVELOPER_ID),
                                   path, message, parse_mode='HTML')

            photo_id = photo.json['photo'][0]['file_id']

            for el in User.objects.values_list('id',).exclude(id=DJANGO_DEVELOPER_ID):
                try:
                    bot.send_photo(el[0], photo_id, message,
                                   parse_mode='HTML')
                except Exception as e:
                    print("ID неправылный или бота заблокировал ")

        return super(MailingsAdmin, self).response_post_save_add(
            request, obj)

    list_display = ("message", "date_sent", "image", "portfolio",)
    list_per_page = 50
    action_form = CustomActionForm


@ admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username",
                    "phone_number", "subscription_status", "date_joined", "subscribed_until")
    exclude = ("number_of_subscriptions", "portfolio")
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
