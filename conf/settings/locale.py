import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-h1c$5#$j+=a!gk@o(2=u+)+eibewxl3vn-_1e-(bs32!p43smu'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))
MEDIA_URL = "/media/"

STATIC_URL = '/static/'
STATIC_ROOT = Path(BASE_DIR).joinpath('static')
# STATICFILES_DIRS = [Path(BASE_DIR).joinpath('static')]

from conf.settings.base import *
