# Generated by Django 4.2.4 on 2023-10-08 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_descriptionimage_descriptionpoint_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductFeatureOption',
            new_name='ProductFeaturePoint',
        ),
    ]