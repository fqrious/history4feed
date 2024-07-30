"""
Django settings for history4feed project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from textwrap import dedent

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'django.contrib.postgres',
    'history4feed.app',
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

ROOT_URLCONF = 'history4feed.urls'

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

WSGI_APPLICATION = 'history4feed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),            # Database name
        'USER': os.getenv('POSTGRES_USER'),          # Database user
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),  # Database password
        'HOST': 'pgdb',                              # PostgreSQL service name in Docker Compose
        'PORT': '5432',                              # PostgreSQL default port
    },
    'sqlite': {
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'history4feed.app.autoschema.H4FSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}


SPECTACULAR_SETTINGS = {
    'TITLE': "history4feed API",
    'DESCRIPTION': dedent("""
        history4feed can be used to create a complete history for a blog and output it as an RSS feed.
    """),
    'VERSION': '1.0.0',
    'CONTACT': {
        'email': 'noreply@dogesec.com',
        'url': 'https://github.com/muchdogesec/history4feed',
    },
    'TAGS': [
        {
            "name": "Feeds",
            "description": "Subscribe and retrieve blogs and blog posts"
        },
        {
            "name": "Jobs",
            "description": "Check the status of data retrieval from blogs"
        },
    ],

}

SCRAPFLY_KEY = os.getenv("SCRAPFLY_APIKEY")
# H4F_CONCURRENT_TASKS = 1 if not SCRAPFLY_KEY else 20
WAYBACK_BACKOFF_TIME = os.getenv("WAYBACK_BACKOFF_TIME") #should be at least 20 seconds because wayback usually blocks your IP for a few minutes

EARLIEST_SEARCH_DATE = datetime.strptime(os.environ["EARLIEST_SEARCH_DATE"], "%Y-%m-%dT%H:%M:%SZ")
WAYBACK_SLEEP_SECONDS = int(os.getenv("WAYBACK_SLEEP_SECONDS", 20))
REQUEST_RETRY_COUNT = int(os.getenv("REQUEST_RETRY_COUNT", 3))

DEFAULT_PAGE_SIZE = os.getenv("DEFAULT_PAGE_SIZE", 50)
MAX_PAGE_SIZE = os.getenv("MAX_PAGE_SIZE", 50)

HISTORY4FEED_NAMESPACE = "6c6e6448-04d4-42a3-9214-4f0f7d02694e"