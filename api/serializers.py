from rest_framework import serializers
from app.models import Promo, User, Portfolio


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username",
                  "phone_number", "subscription_status", "language", "date_joined")

class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = "__all__"


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = "__all__"