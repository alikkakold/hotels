# Generated by Django 2.2.2 on 2020-06-07 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor_app', '0006_auto_20200607_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='date_of_expiry',
            field=models.DateField(default=datetime.datetime(2021, 6, 7, 16, 47, 21, 142338)),
        ),
    ]
