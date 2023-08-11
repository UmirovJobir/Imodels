# Generated by Django 4.2.4 on 2023-08-11 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_en',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_ru',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_uz',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='productvideo',
            name='title',
            field=models.TextField(max_length=500),
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('additional_desc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='additional_description', to='shop.additionaldescription')),
            ],
        ),
        migrations.AddField(
            model_name='additionaldescription',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_description', to='shop.product'),
        ),
    ]
