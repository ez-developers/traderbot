from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.IntegerField(null=True)
    joined = models.DateTimeField(null=True)

class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField(null=True)
    price = models.PositiveBigIntegerField(null=True, blank=True)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, null=True, blank=True)
    paid = models.BooleanField(default=False)
