from django.contrib import admin
from .models import User, Promo, Portfolio, VideoLesson, Mailings
from .forms import CustomActionForm

admin.site.site_url = None
admin.site.index_title = "Добро пожаловать!"
admin.site.site_title = "Администрация «Trader Bot»"
admin.site.site_header = "Администрация «Trader Bot»"


@admin.register(User)
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


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ("promo_id", "valid_date", "is_active")
    readonly_fields = ("promo_id", "is_active")
    list_per_page = 50
    action_form = CustomActionForm

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("name",)
    exclude = ("users_list", "users_count")
    actions_selection_counter = True
    action_form = CustomActionForm
    list_per_page = 50


@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_per_page = 50
    action_form = CustomActionForm

@admin.register(Mailings)
class MailingsAdmin(admin.ModelAdmin):
    list_display = ("message", "date_sent", "portfolio",)
    list_per_page = 50
    action_form = CustomActionForm