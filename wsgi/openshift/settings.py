"""
Django settings for openshift project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# Build paths inside the project like this: os.path.join(PROJECT_DIR, ...)
import os
import imp

# introspect from openshift
ON_OPENSHIFT = False
if os.environ.get('OPENSHIFT_REPO_DIR', False):
    ON_OPENSHIFT = True
DB_USER = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME', None)
DB_PASSWD = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD', None)
# get these from openshift or use localhost versions
DB_NAME = os.environ.get('OPENSHIFT_APP_NAME', "django")
DB_HOST = os.environ.get('OPENSHIFT_MYSQL_DB_HOST', "127.0.0.1")
DB_PORT = os.environ.get('OPENSHIFT_MYSQL_DB_PORT', "3306")

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'ascq#%bii8(tld52#(^*ht@pzq%=nyb7fdv+@ok$u^iwb@2hwh'

default_keys = {
    'SECRET_KEY': 'vm4rl5*ymb@2&d_(gc$gb-^twq9w(u69hi--%$5xrh!xk(t%hw'}
use_keys = default_keys
if ON_OPENSHIFT:
    imp.find_module('openshiftlibs')
    import openshiftlibs
    use_keys = openshiftlibs.openshift_secure(default_keys)

SECRET_KEY = use_keys['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if ON_OPENSHIFT:
    DEBUG = False
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = []
    DEBUG = True

ROOT_URLCONF = 'urls'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'markdown',
    'report',
    'rest_framework',
    'services',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # added for Django 1.10 compliance
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# If you want configure the REDISCLOUD
if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ \
   and 'REDISCLOUD_PASSWORD' in os.environ:
    redis_server = os.environ['REDISCLOUD_URL']
    redis_port = os.environ['REDISCLOUD_PORT']
    redis_password = os.environ['REDISCLOUD_PASSWORD']
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '%s:%d' % (redis_server, int(redis_port)),
            'OPTIONS': {
                'DB': 0,
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'PASSWORD': redis_password,
            }
        }
    }
    MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + \
        MIDDLEWARE_CLASSES + \
        ('django.middleware.cache.FetchFromCacheMiddleware',)
else:  # local caching
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': ''
        }
    }


WSGI_APPLICATION = 'wsgi.application'

TEMPLATES = [
    {
        # 'DEBUG':DEBUG,
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/home/ugr/GitHub/webapp/wsgi/openshift/report/templates/',
            os.path.join(PROJECT_DIR, 'templates'),
            os.path.join(PROJECT_DIR, 'report/templates')
        ],
        'APP_DIRS': True,
        # 'LOADERS': [
        #     'django.template.loaders.filesystem.Loader',
        #     'django.template.loaders.app_directories.Loader',
        #     'django.template.loaders.eggs.Loader',
        # ],
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
            ]
        },
    },
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.DjangoFilterBackend'
    ],
    'PAGE_SIZE': 100,
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if ON_OPENSHIFT or (DB_USER and DB_PASSWD):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
if 'OPENSHIFT_REPO_DIR' in os.environ:
    STATIC_ROOT = os.path.join(os.environ.get(
        'OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
else:
    STATIC_ROOT = os.path.abspath(os.path.join(
        PROJECT_DIR, '..', STATIC_URL.strip("/")))

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("js", os.path.join(STATIC_ROOT, 'js')),
    ("css", os.path.join(STATIC_ROOT, 'css')),
    # ("images", os.path.join(STATIC_ROOT,'images')),
    # ("fonts", os.path.join(STATIC_ROOT,'fonts')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
