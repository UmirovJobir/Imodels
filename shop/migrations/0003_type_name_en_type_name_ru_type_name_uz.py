# Generated by Django 4.2.4 on 2023-12-06 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_description_title_alter_description_title_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='name_en',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='type',
            name='name_ru',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='type',
            name='name_uz',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
