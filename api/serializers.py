from rest_framework import serializers
from app.models import Promo, User, Portfolio, VideoLesson


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
            "users_list"
        )


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = "__all__"


class VideoLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLesson
        fields = "__all__"
