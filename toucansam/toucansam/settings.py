# Django settings for toucansam project.
import dj_database_url
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
GRAPPELLI_ADMIN_TITLE = "Toucan Sam"

DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost/haikubattle')
}

TOUCAN_COLORS = [
    '#FFD700', #gold
    '#FF00FF', #fuchsia
    '#FF69B4', #hotpink
    '#00FF00', #lime
    '#FF4500', #orangered
    '#FF0000', #red
    '#A0522D', #sienna
    '#9932CC' #darkorchid
]

import os
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# cachebusting
gitdescr = os.popen("git describe --always")
GIT_TAG = gitdescr.read().strip()
gitdescr.close()

MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/%s/admin/' % GIT_TAG

# Additional locations of static files
STATICFILES_DIRS = (
    "static",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r@a4bz0=hfe$_fs-yz=2d(l7&amp;q$75o0$t-pp2qj%e)_p^j(r$p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'toucansam.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'toucansam.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'south',
    'toucansam',
    'core',
    'grappelli',
    'django.contrib.admin',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "lib.context_processors.config",
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


try:
    from local_settings import *
except ImportError:
    print ("No local settings found, or it errored")

try:
    MIDDLEWARE_CLASSES += ADDITIONAL_MIDDLEWARE_CLASSES
except NameError:
    pass
