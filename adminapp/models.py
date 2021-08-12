from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.IntegerField(null=True)
    subscription = models.BooleanField(null=True, default=False)
    joined = models.DateTimeField(null=True)



