# Generated by Django 4.2.4 on 2023-09-28 06:59

import account.managers
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0014_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="Faqat o'zbek raqamlarigina tasdiqlanadi", regex='^998[0-9]{2}[0-9]{7}$')], verbose_name='Telefon raqam')),
                ('eskiz_id', models.CharField(blank=True, max_length=20, null=True)),
                ('key', models.CharField(max_length=100, null=True)),
                ('eskiz_code', models.CharField(blank=True, max_length=6, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
            managers=[
                ('objects', account.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuthSms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secure_code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='authsms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Auth Sms',
                'verbose_name_plural': 'Auth Sms',
            },
        ),
    ]
