# Generated by Django 3.2.8 on 2021-10-28 16:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20211028_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentcontrol',
            name='for_day',
            field=models.DateField(default=datetime.datetime(2021, 10, 28, 16, 19, 53, 408907, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='qr_code',
            field=models.TextField(default='MOP7HnC5BzpE3SaR', verbose_name='unique code QR'),
        ),
    ]
