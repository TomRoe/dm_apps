"""
Django settings for glf_sci_site project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from . import media_conf

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')
MEDIA_DIR = os.path.join(BASE_DIR,'media')

# Custom variables
MY_ENVR = media_conf.where_am_i()
MY_CNF = os.path.join(BASE_DIR,'my.cnf')
WEB_APP_NAME = "GulfScienceDataManagement"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***REMOVED***'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['glfscidm001','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap4',
    'accounts',
    'dm_tickets',
    'inventory',
    'bugs',
    'grais',
    'docs',
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

ROOT_URLCONF = 'glf_sci_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'glf_sci_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

#for mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'TIME_ZONE':'America/Halifax',
        'OPTIONS': {
            'read_default_file':MY_CNF,
            'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}

# FOR SQLLITE
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
#
# # FOR ORACLE 12
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.oracle',
#         'NAME': 'PTRAN',
#         'USER': 'glf_science',
#         'PASSWORD': 'Gulf4Ever#',
#         'HOST': '',
#         'PORT': '',
#         'OPTIONS': {
#             'threaded': True,
#             'use_returning_into': False,
#             },
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

#Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 587
EMAIL_PORT = 25
EMAIL_USE_TLS = False

LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Halifax'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

if MY_ENVR == "dev":
    STATICFILES_DIRS = [
    STATIC_DIR,
    ]
else:
    STATIC_ROOT = STATIC_DIR
