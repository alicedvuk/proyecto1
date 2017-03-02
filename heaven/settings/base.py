"""
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
# -*- encoding: utf8 -*-

import os

from heaven.core.utils import load_environment_file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
location = lambda path: os.path.abspath(os.path.join(BASE_DIR, path))

load_environment_file(location('environment.ini'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '*$c111!$&*g#9pkyszumk!)fu7g6wae7a+i8x%&+p26_e)92b*'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split()

SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'sorl.thumbnail',
    'storages',
    'ckeditor',
    'captcha',

    'heaven.girls',
    'heaven.escort_profile',
    'heaven.core.apps.CoreConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'heaven.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [location('heaven/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'vv.configuration.context_processors.siteconfiguration',
            ],
        },
    },
]

WSGI_APPLICATION = 'heaven.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DJANGO_DATABASE_NAME', 'd56js4lrvmi2v'),
        'HOST': os.environ.get('DJANGO_DATABASE_HOST', 'ec2-54-228-246-19.eu-west-1.compute.amazonaws.com'),
        'USER': os.environ.get('DJANGO_DATABASE_USER', 'pfjrrpkplbizbz'),
        'PORT': '5432',
        'PASSWORD': 'pR_CaV6vZgeiuw4Bh_--m2X48w',
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': True,
    }
}



# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

THUMBNAIL_DEBUG = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = location('../public/media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    location('heaven/statics'),
]
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'heaven/public/static')

#Amazon AWS S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJHH2JPYEI42VN3RA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = '123-london'
AWS_S3_SECURE_URLS = True
AWS_IS_GZIPPED = True
AWS_QUERYSTRING_AUTH = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#CKEDITOR
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 350,
        'width': 650,
    },
}

#ReCapcha
RECAPTCHA_PUBLIC_KEY = '6LdLZycTAAAAADb6hh7oIU0cYIRgOLetDHIOaKoV'
RECAPTCHA_PRIVATE_KEY = '6LdLZycTAAAAAIeVTZ2I1MB2HgGWES1kF0NSy6qW'
NOCAPTCHA = True

#SendGrid
EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = "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"