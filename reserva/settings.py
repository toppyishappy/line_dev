from .common_settings import *  # pylint: disable=W0401


INSTALLED_APPS += [
    'line',
    'history',
    'accounts',
    'corsheaders',
    'rest_framework',
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.custom_error.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

try:
    from configs import *  # pylint: disable=W0401
except ImportError:
    pass

AUTH_USER_MODEL = 'accounts.User'

CHANNEL_SECRET = getattr(configs, 'CHANNEL_SECRET', None)
CHANNEL_ACCESS_TOKEN = getattr(configs, 'CHANNEL_ACCESS_TOKEN', None)

CORS_ALLOW_ALL_ORIGINS = True