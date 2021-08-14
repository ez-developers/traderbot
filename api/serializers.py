from rest_framework import serializers
from app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username",
                  "phone_number", "subscription_status", "language", "date_joined")
