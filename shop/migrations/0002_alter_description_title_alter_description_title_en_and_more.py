# Generated by Django 4.2.4 on 2023-11-30 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='description',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Tavsif sarlavhasi'),
        ),
        migrations.AlterField(
            model_name='description',
            name='title_en',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Tavsif sarlavhasi'),
        ),
        migrations.AlterField(
            model_name='description',
            name='title_ru',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Tavsif sarlavhasi'),
        ),
        migrations.AlterField(
            model_name='description',
            name='title_uz',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Tavsif sarlavhasi'),
        ),
    ]
