# Generated by Django 3.2.8 on 2021-11-27 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0019_auto_20211124_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeemanagement',
            name='code',
            field=models.CharField(blank=True, default='q6UmTd9o', max_length=255, verbose_name='kode spv'),
        ),
        migrations.AlterField(
            model_name='invitationlink',
            name='link',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='invitationlink',
            name='spv',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invitationlink',
            name='valid_until',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='qr_code',
            field=models.TextField(default='ualGw7dWIDVZ6PFs', verbose_name='unique code QR'),
        ),
    ]
