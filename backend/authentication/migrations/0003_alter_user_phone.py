# Generated by Django 4.0.6 on 2022-07-17 10:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_rename_verified_user_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+91'. Up to 13 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
