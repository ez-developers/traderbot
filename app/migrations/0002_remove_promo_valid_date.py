# Generated by Django 3.2.6 on 2021-08-25 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promo',
            name='valid_date',
        ),
    ]
