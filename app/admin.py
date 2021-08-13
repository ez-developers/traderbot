from django.contrib import admin
from .models import User

admin.site.site_url = None
admin.site.index_title = "Добро пожаловать!"
admin.site.site_title = "Администрация «Trader Bot»"
admin.site.site_header = "Администрация «Trader Bot»"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username",
                    "phone_number", "subscription_status")
    list_display_links = ("id",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
