# Generated by Django 3.2.8 on 2021-11-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_auto_20211123_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeemanagement',
            name='code',
            field=models.CharField(blank=True, default='X7ifEVv8', max_length=255, verbose_name='kode spv'),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='qr_code',
            field=models.TextField(default='hMKTNpAeubBGv9YO', verbose_name='unique code QR'),
        ),
    ]