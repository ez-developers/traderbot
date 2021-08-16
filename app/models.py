from django.utils.crypto import get_random_string
from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

# Create your models here.


class User(models.Model):
    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    LANGUAGES = [
        ('en', "English"),
        ('ru', "Русский")
    ]

    id = models.BigIntegerField(primary_key=True, verbose_name="ID")
    first_name = models.CharField(
        max_length=255, null=True, verbose_name="Имя", blank=True)
    last_name = models.CharField(
        max_length=255, null=True, verbose_name="Фамилия", blank=True)
    username = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Юзернейм")
    phone_number = models.PositiveBigIntegerField(
        null=True, verbose_name="Телефон", blank=True)
    subscription_status = models.BooleanField(
        null=False, default=False, verbose_name="Статус подписки")
    language = models.CharField(
        max_length=2, choices=LANGUAGES, default=None, null=True, verbose_name="Язык")
    date_joined = models.DateField(
        null=True, verbose_name="Дата присоединения", auto_now_add=True)
    portfolio = models.ManyToManyField(
        'Portfolio', verbose_name="Портфели пользователя")

    def __str__(self):
        return str(self.id)


class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField(null=True)
    price = models.PositiveBigIntegerField(null=True, blank=True)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, null=True, blank=True)
    paid = models.BooleanField(default=False)


class Promo(models.Model):
    RANDOM_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    unique_id = get_random_string(length=6, allowed_chars=RANDOM_CHARS)
    promo_id = models.CharField(
        max_length=255, default=unique_id, null=True, blank=True, unique=True, verbose_name="Промокод")
    valid_date = models.DateField(default=datetime.now(
    )+timedelta(days=365),  verbose_name="Действителен до")
    is_active = models.BooleanField(default=True, verbose_name="Активный")

    def __str__(self):
        return self.promo_id

    class Meta:
        verbose_name_plural = "Промокоды"
        verbose_name = "Промокод"


class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name="Название портфеля")

    class Meta:
        verbose_name_plural = "Портфели"
        verbose_name = "Портфель"

    def __str__(self):
        return self.name
