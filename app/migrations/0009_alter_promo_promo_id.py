# Generated by Django 3.2.6 on 2021-08-13 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_promo_promo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='promo_id',
            field=models.CharField(blank=True, default='TLQEMF', editable=False, max_length=255, null=True, unique=True),
        ),
    ]
