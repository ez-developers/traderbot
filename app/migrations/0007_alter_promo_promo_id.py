# Generated by Django 3.2.6 on 2021-08-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210813_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='promo_id',
            field=models.CharField(blank=True, default='G4V9XR43OHZZS0BK270018T92VB5YYO2', editable=False, max_length=255, null=True, unique=True),
        ),
    ]
