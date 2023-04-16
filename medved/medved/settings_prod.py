DEBUG = False
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db2',
        'USER': 'django_shop2',
        'PASSWORD': 'django_shop_test2',
        'HOST': 'localhost',
        'PORT': '',         # Set to empty string for default.
    }
}
