"""
Django settings for imodels project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")


INTERNAL_IPS = [
    "127.0.0.1",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

CORS_ALLOWED_ORIGINS = [
    "http://jobir.uz",
    "https://jobir.uz",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]


# Application definition
INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #app
    'account',
    'shop',

    #packages
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'embed_video',
    'django_summernote',
    'nested_admin',
    'debug_toolbar',
    'django_filters',
    'django_cleanup',
    'admin_reorder',
    'rangefilter',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', #debug_toolbar
    'imodels.middleware.ModelAdminReorderWithNav', #admin_reorder
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', #cors
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'imodels.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'imodels.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'account.User'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/


TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'backend/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 


LANGUAGES = (
    ('uz', 'Lotin'),
    ('ru', 'Russian'),
    ('en', 'English'),
)

LANGUAGE_CODE = 'uz'
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('uz', 'ru', 'en'),
    'ru': ('ru',),
    'en': ('en',)
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5MB

SUMMERNOTE_CONFIG = {
    'summernote': {
        'airMode': False,
        'width': '1200px',
        'height': '500px',
    }
}


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SPECTACULAR_SETTINGS = {
    "TITLE": "iModels API",
    "DESCRIPTION": "iModels shop",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


CART_SESSION_ID = 'cart'
SESSION_COOKIE_AGE = 86400
SESSION_ENGINE = 'django.contrib.sessions.backends.db'


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.template.context_processors.request',
)

# JAZZMIN_SETTINGS = {
#     "site_title": "Imodels Admin Panel",
#     "site_header": "Imodels",
#     "site_brand": "Imodels",
#     "site_logo": "img/imodels.jpg",
#     "login_logo": None,
#     "login_logo_dark": None,
#     "site_logo_classes": "img-circle",
#     "site_icon": "img/imodels.jpg",
#     "welcome_sign": "Welcome to the Imodels Admin Panel",
#     "changeform_format": "single",
# }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1), #minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1)
}


MYSERVICE = {
    'telebot': {
        'base_url': env.str('TELEBOT_URL'),
        'token': env.str('TELEBOT_TOKEN'),
        'chat_id': {
            "chat_id_orders": env.str('TELEBOT_CHAT_ID_ORDERS'),
            "chat_id_warnings": env.str('TELEBOT_CHAT_ID_CONTACTS'),
        }
    },
    'sms_service': {
        'api_url': env.str('SMS_URL'),
        'email': env.str('SMS_EMAIL'),
        'password': env.str('SMS_PASSWORD')
    }
}

PASSWORD_RESET_TIMEOUT = 10800


ADMIN_REORDER = (
    {'app': 'account', 'label': 'Admin',
     'models': (
        {'model': 'auth.Group', 'label': 'Adminstratorlar guruhlari'},
        {'model': 'account.User', 'label': 'Foydalanuvchilar'},
    )},

    {'app': 'account', 'label': 'Yuborilgan SMS lar',
     'models': (
        {'model': 'account.AuthSms', 'label': 'Tasdiqlash kodlar'},
    )},

    {'app': 'shop', 'label': "Blog",
     'models': ('shop.Blog',)
    },

    {'app': 'shop', 'label': "Product",
     'models': (
        {'model': 'shop.Category', 'label': 'Kategoriyalar'},
        {'model': 'shop.Product', 'label': 'Mahsulotlar'},
        {'model': 'shop.Sale', 'label': 'Chegirma Mahsulotlar'},
    )},

    {'app': 'shop', 'label': 'Order and Contact',
     'models': (
        {'model': 'shop.Order', 'label': 'Buyurtmalar'},
        {'model': 'shop.ContactRequest', 'label': 'Murojatlar'},
    )},

    {'app': 'django_summernote', 'label': 'Summernote',
    'models': (
        'django_summernote.Image',
        'django_summernote.Attachment',
    )},
)