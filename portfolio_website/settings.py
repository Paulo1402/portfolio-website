"""
Django settings for portfolio_website project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

import decouple
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = decouple.config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = decouple.config("DJANGO_DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = decouple.config("DJANGO_ALLOWED_HOSTS", cast=decouple.Csv())

CSRF_TRUSTED_ORIGINS = decouple.config(
    "DJANGO_CSRF_TRUSTED_ORIGINS", cast=decouple.Csv()
)

# Application definition

INSTALLED_APPS = [
    # "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
    "tagulous",
    "parler",
    "rosetta"
]

SERIALIZATION_MODULES = {
    "xml": "tagulous.serializers.xml_serializer",
    "json": "tagulous.serializers.json",
    "python": "tagulous.serializers.python",
    "yaml": "tagulous.serializers.pyyaml",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    
    'django.middleware.locale.LocaleMiddleware',

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio_website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio_website.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Database configuration
if decouple.config("DJANGO_ENV") == "production":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": decouple.config("POSTGRES_DB"),
            "USER": decouple.config("POSTGRES_USER"),
            "PASSWORD": decouple.config("POSTGRES_PASSWORD"),
            "HOST": decouple.config("POSTGRES_HOST"),
            "PORT": decouple.config("POSTGRES_PORT", "5432"),
        }
    }
    print("🎲 Starting Django on PostgreSQL")
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    print("🎲 Starting Django on SQLite")

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

# TODO: add support to english by using https://django-parler.readthedocs.io/en/stable/
USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("en", _("English")),
    ("pt-br", _("Portuguese")),
)

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Parler settings
PARLER_LANGUAGES = {
    None: (
        {"code": "en", "name": _("English")},
        {"code": "pt-br", "name": _("Portuguese")},
    ),
    "default": {
        "fallbacks": ["en", "pt-br"],
        "hide_untranslated": False,
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Project variables
GITHUB_TOKEN = decouple.config("GITHUB_TOKEN")
