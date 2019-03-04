import os
from .base import *  # noqa
from .base import env

print('#'*60)
print('ZAPPADEV config')
print('#'*60)

# zappa specific
# ==============

# prefetch the environment variables - must be defined in lambda console
ZAPPA_DEBUG = env('ZAPPA_DEBUG', default=False)
ZAPPA_GATEWAY_HOST = env('ZAPPA_GATEWAY_HOST', default='BACK-unspecified.com')
ZAPPA_GATEWAY_HOST_FRONT = env('ZAPPA_GATEWAY_HOST_FRONT', default='FRONT-unspecified.com')
ZAPPA_SECRET_KEY = env('ZAPPA_SECRET_KEY', default='missing - temp key.. as;dky6yasdkjfytsyAY!Ekhodfkjbasdjfypj12368u$%@(#$^naddflkjh')


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = ZAPPA_DEBUG
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = ZAPPA_SECRET_KEY
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]
ALLOWED_HOSTS += [ZAPPA_GATEWAY_HOST]
ALLOWED_HOSTS += [ZAPPA_GATEWAY_HOST_FRONT]


# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa F405

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'localhost'
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ['debug_toolbar']  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']


# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ['django_extensions']  # noqa F405
INSTALLED_APPS += ['behave_django']  # noqa F405


# Your stuff...
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['zappa_django_utils']

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin/')
print('#'*60)
print(f'ADMIN_URL: {ADMIN_URL}')
print('#'*60)


# zappa specific
# ==============

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ursula',
        'USER': 'postgres',
        'PASSWORD': env('ZAPPA_DATABASE_POSTGRES_PASSWORD'),
        'HOST': env('ZAPPA_DATABASE_POSTGRES_HOST'),
        'PORT': '5432',
    }
}

DATABASES['default']['ATOMIC_REQUESTS'] = True


# STORAGES
# ------------------------------------------------------------------------------
# https://github.com/etianen/django-s3-storage
INSTALLED_APPS += ['django_s3_storage']  # noqa F405
# zappa-hari-umfrage-s3-access
AWS_REGION = "eu-central-1"
AWS_ACCESS_KEY_ID = env('ZAPPA_S3_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('ZAPPA_S3_AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = env('ZAPPA_S3_AWS_STORAGE_BUCKET_NAME')
AWS_S3_BUCKET_NAME_STATIC = AWS_S3_BUCKET_NAME
_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
}


# STATIC
# ------------------------

STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
STATIC_URL = f'https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/static/'
AWS_S3_BUCKET_AUTH_STATIC = False


# MEDIA
# ------------------------------------------------------------------------------

# # region http://stackoverflow.com/questions/10390244/
# # Full-fledge class: https://stackoverflow.com/a/18046120/104731
# from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402
#
#
# class StaticRootS3Boto3Storage(S3Boto3Storage):
#     location = 'static'
#
#
# class MediaRootS3Boto3Storage(S3Boto3Storage):
#     location = 'media'
#     file_overwrite = False


# endregion
DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
MEDIA_URL = f'https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/media/'

