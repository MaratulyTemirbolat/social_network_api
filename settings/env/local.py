from settings.base import *  # noqa


# ----------------------------------------------------------
#
DEBUG = True
WSGI_APPLICATION = None
ASGI_APPLICATION = 'deploy.test.asgi.application'

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

# ----------------------------------------------------------
#
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],
#         },
#     },
# }
