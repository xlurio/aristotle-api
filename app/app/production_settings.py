"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from . import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")


DEBUG = False


ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = settings.INSTALLED_APPS

MIDDLEWARE = settings.MIDDLEWARE

ROOT_URLCONF = settings.ROOT_URLCONF

TEMPLATES = settings.TEMPLATES

WSGI_APPLICATION = settings.WSGI_APPLICATION


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = settings.AUTH_PASSWORD_VALIDATORS


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = settings.LANGUAGE_CODE

TIME_ZONE = settings.TIME_ZONE

USE_I18N = settings.USE_I18N

USE_TZ = settings.USE_TZ


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = settings.STATIC_URL
MEDIA_URL = settings.MEDIA_URL

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = settings.DEFAULT_AUTO_FIELD

# Authentication

AUTH_USER_MODEL = settings.AUTH_USER_MODEL

# Caching

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": (
            f"redis://{os.environ.get('CACHE_BACKEND_HOST')}:"
            f"{os.environ.get('CACHE_BACKEND_PORT')}"
        ),
    }
}

# Django REST Framework

REST_FRAMEWORK = settings.REST_FRAMEWORK

# Security

is_deploy = os.environ.get("IS_DEPLOY", 0)

if is_deploy == 1:
    SECURE_HSTS_SECONDS = 259200
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
