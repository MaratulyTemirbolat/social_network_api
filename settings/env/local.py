from settings.base import *  # noqa


# ----------------------------------------------------------
#
DEBUG = True
WSGI_APPLICATION = None

# ----------------------------------------------------------
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]
INTERNAL_IPS = [
    '127.0.0.1',
]

# ----------------------------------------------------------
#
INSTALLED_APPS += [  # noqa
    'debug_toolbar',
]
MIDDLEWARE += [  # noqa
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
