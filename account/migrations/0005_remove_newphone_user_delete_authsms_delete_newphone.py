# Generated by Django 4.2.4 on 2024-06-10 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_expiration_time_user_new_phone_temp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newphone',
            name='user',
        ),
        migrations.DeleteModel(
            name='AuthSms',
        ),
        migrations.DeleteModel(
            name='NewPhone',
        ),
    ]
