# Generated by Django 5.2 on 2025-04-24 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]
