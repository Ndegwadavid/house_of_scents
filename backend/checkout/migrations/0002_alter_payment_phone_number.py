# Generated by Django 5.2 on 2025-04-27 07:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=12, validators=[django.core.validators.RegexValidator(message='Phone number must be in the format +254XXXXXXXXX', regex='^\\+254\\d{9}$')]),
        ),
    ]
