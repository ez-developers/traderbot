# Generated by Django 3.2.6 on 2021-08-24 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_alter_promo_promo_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcast',
            name='to_all',
        ),
    ]
