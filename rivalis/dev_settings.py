"""Development settings"""
from .shared_settings import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Rivalis
    'www.apps.WwwConfig',
    'users.apps.UsersConfig',
    'organizations.apps.OrganizationsConfig',
    'disciplines.apps.DisciplinesConfig',
    'tournaments.apps.TournamentsConfig',
    # Packages
    'django_cleanup.apps.CleanupConfig',
    'django_extensions',
]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}


# Emails

# Prints the email content in the terminal
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
