# Generated by Django 3.0.6 on 2020-05-30 07:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor_app', '0002_auto_20200530_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='date_of_expiry',
            field=models.DateField(default=datetime.datetime(2021, 5, 30, 10, 30, 45, 109997)),
        ),
    ]
