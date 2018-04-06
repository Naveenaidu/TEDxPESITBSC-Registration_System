import os

from ingenius.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','13.126.226.206','registrations.tedxpesitbsc.com']

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

STATIC_ROOT = os.environ.get('STATIC_ROOT', None)
