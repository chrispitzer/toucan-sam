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

# for SENTRY
#LOCAL_APPS = [
#    'raven.contrib.django'
#]

# SENTRY_DSN = ''

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'registration@toucan.com'
# EMAIL_HOST_PASSWORD = 'tXbJ1DIXGN0dxzdrfqBo'
# EMAIL_USE_TLS = True


