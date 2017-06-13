"""
Django settings for ssme project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from django.core.urlresolvers import reverse_lazy
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'edn95yq=n4a5^7h76l*5%bhom#4wolo$$@&k%r1vjc4xoil*dj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'controlcenter',
    'betterforms',
    'django_tables2',
    'django_extensions',
    'ssme_activities',
    'import_export',
    'rest_framework',
    'django_filters',
    'formtools',
    'guardian',
    'smartmin',
    'explorer',
    'debug_toolbar',
    # import tasks
    'smartmin.csv_imports',
    # smartmin users
    'smartmin.users',
    'authtools',
)

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ssme.urls'

#TEMPLATE_DIRS = (
#    os.path.join(BASE_DIR, 'templates'),
#)


WSGI_APPLICATION = 'ssme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'Africa/Bujumbura'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_PATH,  'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH,  'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

FIXTURE_DIRS = (
   os.path.join(BASE_DIR, 'fixtures'),
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.core.context_processors.request',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'ssme.context_processor.myfacility',
    'ssme.context_processor.google_analytics',
    )

#-----------------------------------------------------------------------------------
# Login / Logout
#-----------------------------------------------------------------------------------
LOGIN_URL = reverse_lazy("login")
LOGOUT_URL = reverse_lazy("logout")
LOGIN_REDIRECT_URL = reverse_lazy("landing")
LOGOUT_REDIRECT_URL = reverse_lazy("landing")

AUTH_USER_MODEL = 'authtools.User'

KNOWN_PREFIXES = {
    'RG': 'SELF_REGISTRATION',
    'SDS': 'STOCK_DEBUT_SEMAINE',
    'SR': 'STOCK_RECU',
    'SF': 'STOCK_FINAL',
    'B': 'BENEFICIAIRE',
    'RUP': 'RUPTURE_STOCK',
    'PC': 'POPULATION_CIBLE',
    'X': 'EXIT',
}

#------------------------------------------------
# Smartim
#----------------------------------------------

# create the smartmin CRUDL permissions on all objects
PERMISSIONS = {
  '*': ('create',   # can create an object
        'read',     # can read an object, viewing it's details
        'update',   # can update an object
        'delete',   # can delete an object,
        'list'),    # can view a list of the objects
}

# assigns the permissions that each group should have, here creating an Administrator group with
# authority to create and change users
GROUP_PERMISSIONS = {
    "Administrator": ('auth.user.*',
        'csv_imports.importtask.*',
        )
}

# this is required by guardian
ANONYMOUS_USER_ID = -1

# Path to locale folder
LOCALE_PATHS = (
      os.path.join(BASE_DIR, 'locale'),
)


# The languages you are supporting
LANGUAGES = (
    ('en', 'English'),   # You need to include your LANGUAGE_CODE language
    ('fr', 'French'),
)

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-12345678-9'
GOOGLE_ANALYTICS_DOMAIN = 'mydomain.com'

INTERNAL_IPS = ('127.0.0.1',)

try:
    from localsettings import *
except ImportError:
    pass

