from rest_framework import serializers
from app.models import Promo, User, Portfolio, VideoLesson
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",
                  "first_name",
                  "last_name",
                  "username",
                  "phone_number",
                  "subscription_status",
                  "subscribed_until",
                  "number_of_subscriptions",
                  "language",
                  "date_joined")


class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = (
            "id",
            "name",
            "users_list",
            "users_count"
        )


class PromoSerializer(serializers.ModelSerializer):
    promo_id = serializers.RegexField(
        re.compile("^[A-Z0-9]*$"), min_length=6, max_length=6)

    class Meta:
        model = Promo
        fields = ("id", "promo_id", "valid_date", "is_active")


class VideoLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLesson
        fields = "__all__"
