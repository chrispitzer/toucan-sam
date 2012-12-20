DEBUG = TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': "live_toucan",                      # Or path to database file if using sqlite3.
        'USER': 'live_toucan',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

MEDIA_ROOT = "/srv/toucan/live/media/"
STATIC_ROOT = "/srv/toucan/live/static/"
CHANNEL_PREFIX = "toucan"
LOCAL_APPS = [
    'raven.contrib.django'
]

# SENTRY_DSN = 'http://9a76e9f9844c4d328710abe08efbc7c5:3ee0050371084b378f5bdb8ca75c1a80@zim.lofiart.com:9000/2'

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'registration@toucan.com'
# EMAIL_HOST_PASSWORD = 'tXbJ1DIXGN0dxzdrfqBo'
# EMAIL_USE_TLS = True


