# Generated by Django 5.2 on 2025-04-27 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0004_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_token',
            field=models.CharField(blank=True, max_length=36, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['verification_token'], name='users_user_verific_b0ac6f_idx'),
        ),
    ]
