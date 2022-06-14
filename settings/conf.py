# ------------------------------------------------
# Environmental vatiables
#
SECRET_KEY = 'django-insecure-9($thm4ymln96+-lvny#(3!ewv_gtgp#evm@e8c*28#rpcc=0r'  # noqa

# ------------------------------------------------
# Custom settings
#
ADMIN_SITE_URL = 'custom_admin/'

# ------------------------------------------------
# Debug toolbar configuration
#
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# ------------------------------------------------
# DRF settings
#
REST_FRAMEWORK = {
   'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser', ),
}


# ------------------------------------------------
# Shell plus configuration
#
SHELL_PLUS_PRE_IMPORTS = [
    ('django.db', ('connection', 'reset_queries', 'connections')),
    ('datetime', ('datetime', 'timedelta', 'date')),
    ('json', ('loads', 'dumps')),
]
SHELL_PLUS_MODEL_ALIASES = {
    'auths': {
        'CustomUser': 'U',
    },
    # 'university': {
    #     'Student': 'S',
    #     'Account': 'A',
    #     'Group': 'G',
    #     'Professor': 'P',
    #     'Homework': 'H',
    #     'File': 'FF',
    # },
}
SHELL_PLUS = 'ipython'
SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000

# ------------------------------------------------
# CORS CONFIGURATION
#
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'accept',
    'authorization',
    'content-type',
    'user-agent',
    'Access-Control-Allow-Origin',
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'PUT',
    'PATCH',
    'POST',
)
