"""
Django settings for ci project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from dotenv import load_dotenv
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fb1gumhacn*%(m_g3ui!kai&ak^9=csr=pj=dmoxrqadi%txu4'

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'account',
    'social_django',
    'crispy_forms',
    'easy_thumbnails',
    'control',
    'project',
    'env',
    'tinymce',
    'rosetta',
]

TINYMCE_DEFAULT_CONFIG = {
	'plugins': 'paste',
	'paste_remove_styles': 'true',
	'paste_remove_styles_if_webkit': 'true',
	'paste_strip_class_attributes': 'all',
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'ci.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ci.wsgi.application'

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'



STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

#STATICFILES_DIRS = ( os.path.join('static'), )
load_dotenv()

DEBUG = os.getenv('DEBUG', False)
USER = os.getenv('USER', 'zdimon')
WORK_DIR = os.getenv('WORK_DIR')
ORIGIN_DIR = os.getenv('ORIGIN_DIR')
SSH_LOGIN = os.getenv('SSH_LOGIN', 'dever')
DOMAIN = os.getenv('DOMAIN')
SSH_PASSWORD = os.getenv('SSH_PASSWORD','12333321')
SSH_PORT = os.getenv('SSH_PORT', '22')
ENV_PATH = os.getenv('ENV_PATH')
PROJECT_PATH = os.getenv('PROJECT_PATH')
DB_PATH = os.getenv('DB_PATH')
FRONTEND_PATH = os.getenv('FRONTEND_PATH')
REDIS_DB = os.getenv('REDIS_DB', '5')
DB_NAME = os.getenv('DB_NAME', '')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '')
DATABASE = os.getenv('DATABASE', 'sqlite')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv(
    'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', "...")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv(
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', "...")
SOCIAL_AUTH_REDIRECT_IS_HTTPS = os.getenv(
    'SOCIAL_AUTH_REDIRECT_IS_HTTPS', False)

STATIC_ROOT = os.getenv(
    'STATIC_ROOT', False)

if not STATIC_ROOT:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/logout'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_USER_MODEL = 'account.Customer'

if DATABASE == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

if DATABASE == 'pg':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': '5432',
        },
    }


CELERY_BROKER_URL = 'redis://localhost:6379/%s' % REDIS_DB
