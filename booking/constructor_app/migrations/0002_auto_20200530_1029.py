# Generated by Django 3.0.6 on 2020-05-30 07:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='date_of_expiry',
            field=models.DateField(default=datetime.datetime(2021, 5, 30, 10, 29, 22, 673796)),
        ),
    ]
