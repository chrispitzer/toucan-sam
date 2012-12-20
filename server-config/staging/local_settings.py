DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': "staging_toucan",                      # Or path to database file if using sqlite3.
        'USER': 'staging_toucan',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

MEDIA_ROOT = "/srv/toucan/staging/media/"
STATIC_ROOT = "/srv/toucan/staging/static/"
CHANNEL_PREFIX = "staging"
DEBUG = TEMPLATE_DEBUG = True


# EMAIL_HOST='smtp.gmail.com'
# EMAIL_HOST_USER = 'test@lofiart.com'
# EMAIL_HOST_PASSWORD='Ra1ner~8'
# EMAIL_USE_TLS=True
DEBUG = TEMPLATE_DEBUG = True

