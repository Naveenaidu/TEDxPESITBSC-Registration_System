import os

from ingenius.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','13.126.226.206','regs.tedxpesitbsc.com']

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_ROOT = os.environ.get('STATIC_ROOT', 'None')
