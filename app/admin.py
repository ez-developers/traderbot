from django.contrib import admin, messages
from core.settings import DJANGO_DEVELOPER_ID, BASE_DIR
from .models import User, Promo, Portfolio, VideoLesson, Broadcast, BroadcastToAll
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

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


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


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):

    def response_add(self, request, obj):
        msg = "Сообщения успешно отправлены пользователям"
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)

    # TODO:
    # 1.remove special characters in image name
    # 2. Add portfolio id to send the specific portfolio subscribed users

    def response_post_save_add(self, request, obj):

        image = request.FILES.get('image')
        message = request.POST.get('message')
        portfolio = request.POST.get('portfolio')

        print(portfolio)

        image_path = open(
            str(BASE_DIR) + f'/uploads/broadcasts/{time.strftime("%Y_%m_%d")}/{image}', "rb")

        photo = bot.send_photo(DJANGO_DEVELOPER_ID,
                               image_path, caption=message)

        photo_id = photo.json['photo'][-1]['file_id']
        target_portfolio = Portfolio.objects.filter(
            pk=portfolio).values('users_list')[0]['users_list']
        print(target_portfolio)

        for i in target_portfolio:
            bot.send_message(i, message)

        return super(BroadcastAdmin, self).response_post_save_add(request, obj)

    list_display = ("message", "date_sent", "image", "portfolio",)
    list_per_page = 50
    action_form = CustomActionForm


@ admin.register(BroadcastToAll)
class BroadcastToAllAdmin(admin.ModelAdmin):

    def response_add(self, request, obj):
        msg = "Сообщения успешно отправлены пользователям"
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)
        
    def response_post_save_add(self, request, obj):
        image = request.FILES.get('image')
        message = request.POST.get('message')

        image_path = open(
            str(BASE_DIR) + f'/uploads/broadcaststoall/{time.strftime("%Y_%m_%d")}/{image}', "rb")
        
        photo = bot.send_photo(DJANGO_DEVELOPER_ID,
                                image_path, caption=message)

        photo_id = photo.json['photo'][-1]['file_id']

        for i in User.objects.values_list("id"):
            try:    
                bot.send_photo(i, photo_id, message, parse_mode='HTML')
            except: 
                raise Exception
            
        return super(BroadcastToAllAdmin, self).response_post_save_add(
            request, obj)

        

