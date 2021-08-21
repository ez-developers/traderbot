from django.utils.crypto import get_random_string
from django.db import models
from datetime import datetime, timedelta
from django.contrib.postgres.fields import ArrayField
from .storage import CustomFileSystemStorage
import pytz


class User(models.Model):
    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "пользователя"

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
    subscribed_until = models.DateField(
        verbose_name="Подписка до", null=True)
    number_of_subscriptions = models.PositiveSmallIntegerField(
        default=0)
    language = models.CharField(
        max_length=2, choices=LANGUAGES, default=None, null=True, verbose_name="Язык")
    date_joined = models.DateField(
        null=True, verbose_name="Дата присоединения", auto_now_add=True)
    portfolio = models.ManyToManyField(
        'Portfolio', verbose_name="Портфели пользователя")

    def __str__(self):
        return str(self.id)


def get_code():
    RANDOM_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return get_random_string(length=6, allowed_chars=RANDOM_CHARS)


def add_one_year():
    return datetime.now(
    )+timedelta(days=365)


class Promo(models.Model):
    promo_id = models.CharField(
        max_length=255, default=get_code,  unique=True, verbose_name="Промокод")
    valid_date = models.DateField(
        default=add_one_year,  verbose_name="Действителен до")
    is_active = models.BooleanField(default=True, verbose_name="Активный")

    def __str__(self):
        return self.promo_id

    class Meta:
        verbose_name_plural = "Промокоды"
        verbose_name = "промокод"


class Portfolio(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name="Название портфеля")
    users_list = ArrayField(models.BigIntegerField(),
                            default=list, blank=True)
    users_count = models.IntegerField(
        default=0, verbose_name="Количество подписанных")

    class Meta:
        verbose_name_plural = "Портфели"
        verbose_name = "портфель"

    def __str__(self):
        return self.name


class VideoLesson(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, verbose_name="Ccылка")

    class Meta:
        verbose_name_plural = "Видеоуроки"
        verbose_name = "видеоурок"

    def __str__(self):
        return str(self.id)


class Mailings(models.Model):
    image = models.ImageField(
        upload_to="uploads/mailings/%Y_%m_%d/", storage=CustomFileSystemStorage, null=True, blank=True, verbose_name="Фото")
    message = models.TextField(max_length=4096, verbose_name="Cообщение")
    date_sent = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата отправки")
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Портфель")

    class Meta:
        verbose_name_plural = "Рассылки"
        verbose_name = "рассылку"

    def __str__(self):
        return self.message
