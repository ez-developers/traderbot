from django.db import models

# Create your models here.


class User(models.Model):
    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

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
    date_joined = models.DateField(
        null=True, verbose_name="Дата присоединения", auto_now_add=True)

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
