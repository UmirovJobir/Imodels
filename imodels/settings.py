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
SECRET_KEY = 'ji&^*965bhwao1v8-$(fxmaq(06ghs9ny*gxh(2w&6)d5*&&@#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'jazzmin',
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
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'embed_video',
    'tinymce',
    'nested_admin',
    'debug_toolbar',
    'django_filters',
    'django_cleanup',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', #debug_toolbar
    'django.contrib.sessions.middleware.SessionMiddleware',
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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
   'default': {
        'ENGINE': env.str('POSTGRES_ENGINE'),
        'NAME': env.str('POSTGRES_DB'), 
        'USER': env.str('POSTGRES_USER'), 
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),    
        'PORT': env.str('POSTGRES_PORT')
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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/


TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 


LANGUAGES = (
    ('uz', _('Lotin')),
    ('ru', _('Russian')),
    ('en', _('English')),
)

LANGUAGE_CODE = 'uz'

AUTH_USER_MODEL = 'account.User'

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5MB

TINYMCE_DEFAULT_CONFIG = {
    'custom_undo_redo_levels': 100,
    'selector': 'textarea',
    "menubar": "file edit view insert format tools table help",
    'plugins': 'link image preview codesample contextmenu table code lists fullscreen',
    'toolbar1': 'undo redo | backcolor casechange permanentpen formatpainter removeformat formatselect fontselect fontsizeselect',
    'toolbar2': 'bold italic underline blockquote | alignleft aligncenter alignright alignjustify '
               '| bullist numlist | outdent indent | table | link image | codesample | preview code | tiny_mce_wiris_formulaEditor tiny_mce_wiris_formulaEditorChemistry',
    'contextmenu': 'formats | link image',
    'block_formats': 'Paragraph=p; Header 1=h1; Header 2=h2',
    'fontsize_formats': "8pt 10pt 12pt 14pt 16pt 18pt",
    'content_style': "body { font-family: Arial; background: white; color: black; font-size: 12pt}",
    'codesample_languages': [
        {'text': 'Python', 'value': 'python'}, {'text': 'HTML/XML', 'value': 'markup'},],
    'image_class_list': [{'title': 'Fluid', 'value': 'img-fluid', 'style': {} }],
    'width': '1200px',
    'height': '500px',
    'image_caption': True,
    "images_upload_url": "/upload_image/",
    "images_upload_handler": "tinymce_image_upload_handler"
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SPECTACULAR_SETTINGS = {
    "TITLE": "My Site Project API",
    "DESCRIPTION": "My site with shop app and custom auth",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


CART_SESSION_ID = 'cart'
# SESSION_COOKIE_AGE = 5
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_COOKIE_NAME = 'cart'


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.template.context_processors.request',
)

JAZZMIN_SETTINGS = {
    "site_title": "Imodels Admin Panel",
    "site_header": "Imodels",
    "site_brand": "Imodels",
    "site_logo": "img/imodels.jpg",
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": "img/imodels.jpg",
    "welcome_sign": "Welcome to the Imodels Admin Panel"
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1)
}


MYSERVICE = {
    'telebot': {
        'base_url': env.str('TELEBOT_URL'),
        'token': env.str('TELEBOT_TOKEN'),
        'chat_id': {
            "chat_id_orders": env.str('TELEBOT_CHAT_ID_ORDERS'),
            "chat_id_warnings": env.str('TELEBOT_CHAT_ID_WARNINGS'),
        }
    },
    'sms_service': {
        'base_url': env.str('SMS_URL'),
        'email': env.str('SMS_EMAIL'),
        'password': env.str('SMS_PASSWORD'),
        'group': env.str('SMS_GROUP'),
        'callback_url': env.str('SMS_CALLBACK_URL'),
    }
}

PASSWORD_RESET_TIMEOUT = 10800