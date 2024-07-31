"""
Django settings for Online project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from os import getenv
from socket import gethostbyname, gethostname

DJANGO_WEBSITE_ENVIRONMENT = getenv("DJANGO_WEBSITE_ENVIRONMENT")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv(
    'DJ_SECRET_KEY') if DJANGO_WEBSITE_ENVIRONMENT == "PROD" else "MNBVD$%&ujy654DGy5#2wDfGu8&^543EdfGHjki98&^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if DJANGO_WEBSITE_ENVIRONMENT == "PROD" else True

ALLOWED_HOSTS = [
    "mountainbean.online",
    gethostbyname(gethostname())
]
if DJANGO_WEBSITE_ENVIRONMENT != "PROD":
    ALLOWED_HOSTS.append("localhost")

# Application definition

INSTALLED_APPS = [
    'photos',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Online.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Online.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'AEST'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / "uploads"

MEDIA_URL = "/photo_files/"

AWS_STORAGE_BUCKET_NAME = "mountainbean-photos-bucket-shepherds-pie"
AWS_S3_REGION_NAME = "ap-southeast-2"
AWS_ACCESS_KEY_ID = getenv("S3_WRITE_USER_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = getenv("S3_WRITE_SECRET_ACCESS_KEY")

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

STATICFILES_FOLDER = "static"
MEDIAFILES_FOLDER = "media"

STATICFILES_STORAGE = "custom_storages.StaticFileStorage"
DEFAULT_FILE_STORAGE = "custom_storages.MediaFileStorage"
