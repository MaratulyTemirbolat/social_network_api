from settings.base import *  # noqa


# ----------------------------------------------------------
#
DEBUG = False
WSGI_APPLICATION = 'deploy.prod.wsgi.application'

# ----------------------------------------------------------
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db_prod.sqlite3',
    }
}
ALLOWED_HOSTS = []
INTERNAL_IPS = []
