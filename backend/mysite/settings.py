"""Django settings for mysite project."""

import os
from datetime import timedelta
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='fake-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=str, default="").replace(' ', '').split(',')


# Application definition

SITE_ID = config('SITE_ID',cast = int , default = 1)

REST_USE_JWT = True

INSTALLED_APPS = [
    'activities.apps.ActivitiesConfig',
    'chat.apps.ChatConfig',
    'profiles.apps.ProfilesConfig',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'channels',
]

SOCIALACCOUNT_PROVIDERS = {
    "google":{
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {"access_type": "online"}
    }
}

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'allauth.account.middleware.AccountMiddleware',

]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DB_ENGINE = {
#     'mysql': 'django.db.backends.mysql',
#     'tidb': 'django_tidb'
# }

# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.mysql',
#         'ENGINE': DB_ENGINE.get(config('DATABASE_ENGINE', cast=str, default='mysql')),
#         'NAME': config('DATABASE_NAME', default='myDB', cast=str),
#         'USER': config('DATABASE_USER', default='root', cast=str),
#         'PASSWORD': config('DATABASE_PASSWORD', default='password', cast=str),
#         'HOST': config('DATABASE_HOST', default='localhost', cast=str),
#         'PORT': config('DATABASE_PORT', default='3306', cast=str),
        
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config('DATABASE_NAME', default='myDB', cast=str),
#         'USER': config('DATABASE_USER', default='root', cast=str),
#         'PASSWORD': config('DATABASE_PASSWORD', default='password', cast=str),
#         'HOST': config('DATABASE_HOST', default='localhost', cast=str),
#         'PORT': config('DATABASE_PORT', default='3306', cast=str),
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default=config('DATABASE_URL', cast=str)
    )
}

# REQUIRE_SSL = config('REQUIRE_SSL', default=False, cast=bool)

# if REQUIRE_SSL:
#     DATABASES['default']['OPTIONS'] = {
#             'ssl': {
#                 'ca': config('PATH_TO_CA', default="/etc/ssl/cert.pem", cast=str)
#             },
#         }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(name)s [%(levelname)s] %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file-activities': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'activities.log',
            'formatter': 'simple',
        },
        'file-profiles': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'profiles.log',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'activities': {
            'level': "DEBUG",
            'handlers': ['file-activities'],
        },
        'profiles': {
            'level': "DEBUG",
            'handlers': ['file-profiles'],
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'frontend/dist',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Javascript Frontend
CORS_ALLOWED_ORIGINS = config('ALLOWED_CSRF', cast=str, default="http://127.0.0.1:8080, http://localhost:8080").replace(' ', '').split(',')
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-xsrf-token"]

# CSRF Config
CSRF_TRUSTED_ORIGINS = config('ALLOWED_CSRF', cast=str, default="http://127.0.0.1:8080, http://localhost:8080").replace(' ', '').split(',')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"


# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S.%fZ", 
    'EXCEPTION_HANDLER': 'mysite.exc_handler.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'jwt-reauth',
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_SECURE': True,
    'JWT_AUTH_SAMESITE': 'None'
}

# Django Channels
ASGI_APPLICATION = 'mysite.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# media storing
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')