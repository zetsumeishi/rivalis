"""Production settings"""
from .shared_settings import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['rivalis.gg']


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
]


# Emails

EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
