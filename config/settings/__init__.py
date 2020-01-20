import os
from django.utils.translation import gettext_lazy as _
import logging.config
import environ
from easy_thumbnails.conf import Settings as thumbnail_settings

root = environ.Path(__file__) - 3  # three folder back (/project/config/settings/ - 3 = /)
env = environ.Env()
environ.Env.read_env()


ROOT = root
BASE_DIR = ROOT

DEBUG = env.bool('DEBUG', default=False)

ENV = env.str('ENV', default='live')


SECRET_KEY = env('SECRET_KEY', default='jfh0=qe=afsl)kvbqhe)z&&1-gk9b%h#rz1x@sx2j#-ch-tt@t')
# EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.SendgridBackend')
# EMAIL_HOST = env('EMAIL_HOST', default='mail.experina.nl')
# EMAIL_PORT = env('EMAIL_PORT', default=587)
# EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='notification@experina.nl')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='secret')
# EMAIL_HOST_NAME = env('EMAIL_HOST_NAME', default='Notification Center')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default='*')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SENDER_NAME = env('EMAIL_SENDER_NAME', default='Notifications<notification@experina.nl>')
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=False)
EMAIL_USE_SSL = env('EMAIL_USE_SSL', default=False)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party-apps
    'django_admin_generator',
    'django_extensions',
    'easy_thumbnails',
    'image_cropping',
    'ckeditor',
    # 'ckeditor_uploader',

    # local-apps
    'apps.orders',
    'apps.pages',
    'apps.products',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(str(root), "templates"),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.orders.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': env.db('DATABASE_URL', default=f"sqlite:////{os.path.join(BASE_DIR, 'db.sqlite3')}")
}

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

LANGUAGE_CODE = 'nl'
LANGUAGES = (
    ('nl', _('Dutch')),
    ('en', _('English')),
)

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = env('STATIC_ROOT', default=os.path.join(BASE_DIR, 'static'))


MEDIA_URL = '/media/'
MEDIA_ROOT = env('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))

# ************** CUSTOM SETTINGS *************** #

CART_SESSION_ID = 'cart'

if ENV in ['local']:
    STATICFILES_DIRS = [
        env('STATIC_ROOT', default=os.path.join(BASE_DIR, 'static')),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logfile',
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        # 'celery': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': 'celery.log',
        #     'formatter': 'standard',
        #     'maxBytes': 1024 * 1024 * 100,  # 100 mb
        # },
        'console':{
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['console', 'logfile'],
            'propagate': True,
            'level': 'INFO',
        },
        'apps.authentication': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        },
        'apps.patients': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        },
        'apps.pharmacists': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        },
    }
}

logging.config.dictConfig(LOGGING)


USE_THOUSAND_SEPARATOR = True

FORMAT_MODULE_PATH = ['apps.locale.formats']
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'apps', 'locale'),
)


THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

if ENV == 'local':
    # MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    # INSTALLED_APPS += ['debug_toolbar']
    try:
        from .dev import *
    except ImportError:
        pass
