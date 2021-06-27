import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-h1c$5#$j+=a!gk@o(2=u+)+eibewxl3vn-_1e-(bs32!p43smu'

DEBUG = False

ALLOWED_HOSTS = ['debtbook.uz']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'debtbook'),
        'USER': os.getenv('DB_USER', 'debtbook'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'debtbook'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))
MEDIA_URL = "/media/"

STATIC_URL = '/static/'
# STATIC_ROOT = Path(BASE_DIR).joinpath('static')
STATICFILES_DIRS = [Path(BASE_DIR).joinpath('static')]

from conf.settings.base import *
