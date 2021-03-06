"""
Django settings for portnoy project.

"""

import os

from utils import password

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = 'wlbw&o1bup))k%z3n5t!*6n!t&%vjc@_e&^mi*)77wr5ynk9ek'

DEBUG = True
TEMPLATE_DEBUG = True
THUMBNAIL_DEBUG = True
"""
if "decoder JPEG not available":
sudo apt-get install libjpeg-dev
pip install --no-cache-dir -I pillow
"""

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    #python manage.py crontab add
    #python manage.py crontab show
    #python manage.py crontab remove
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'website',
    'board',
    'utils',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'portnoy.urls'

WSGI_APPLICATION = 'portnoy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = ''
STATIC_URL = '/static/'


# Files uploads
MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

# Session age for a month
SESSION_COOKIE_AGE = 2592000

# Crontab
CRONJOBS = (
        ('0 * * * *', 'portnoy.tasks.remove_dead_post'),
        ('0 0 * * *', 'portnoy.tasks.remove_dead_post', {'recently': False}),
)

# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'wyattliang'
EMAIL_HOST_PASSWORD = password.EMAIL_PASSWORD
EMAIL_USE_SSL = True
