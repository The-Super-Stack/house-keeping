# Generated by Django 3.2.8 on 2021-11-23 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0016_auto_20211119_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeemanagement',
            name='code',
            field=models.CharField(blank=True, default='LZU6vdkz', max_length=255, verbose_name='kode spv'),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='qr_code',
            field=models.TextField(default='mtBrQ15FEqiNxdLT', verbose_name='unique code QR'),
        ),
        migrations.CreateModel(
            name='InvitationLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.SlugField(max_length=255, unique=True)),
                ('valid_until', models.DateTimeField()),
                ('spv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
