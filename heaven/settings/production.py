from .base import *  # flake8: NOQA
import raven

DEBUG = True

AUTH_PASSWORD_VALIDATORS = []


INSTALLED_APPS += (
    #'raven.contrib.django.raven_compat',
)

#EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

#EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', 'email-smtp.us-east-1.amazonaws.com')
#EMAIL_PORT = os.environ.get('DJANGO_EMAIL_PORT', 465)
#EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS ', True)
#EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER ', 'AKIAIWUQRW4UYLZ44JQA')
#EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD', 'AsBqtyBSIt49fBQJUG9gyzXcbJBvhbkgoUCFN4Upygug')
#Raven is a Python client for Sentry. It provides full out-of-the-box support for 
#many of the popular frameworks, including Django, and Flask. Raven also includes drop-in support for any WSGI-compatible web application.
#RAVEN_DSN = os.environ.get(
#    'DJANGO_RAVEN_DSN',
#    'http://8332ac9eea5b482d880ad8fbf963a3e6:06a13dc853044d648b1b71afb17be321@sentry.humanzilla.com/13'
#)

#RAVEN_CONFIG = {'dsn': RAVEN_DSN, 'release': raven.fetch_git_sha(location('..'))}
