from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import TIMEZONES
from .managers import UserManager


class User(AbstractUser):
    """Extension of the Django User model

    Attributes:
        email: Email of the user
        riot_id: A string representing the Riot username of the player
        riot_tag: A string representing the tag associated with the riot_id
        avatar: Image used as a profile picture
        timezone: Datetime object used to display the right date and time to the user
    """

    email = models.EmailField('Email', unique=True)
    riot_id = models.CharField('Riot ID', max_length=255, blank=True)
    riot_tag = models.CharField('Riot Tag', max_length=255, blank=True)
    avatar = models.ImageField(
        'Avatar',
        upload_to='avatars/',
        default='avatars/default.png',
    )
    timezone = models.CharField(
        'Timezone',
        max_length=64,
        choices=TIMEZONES,
        default='UTC',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """String representation of a User object."""

        return f'{self.email}'

    @property
    def full_riot_id(self):
        """Combines the riot_id and riot_tag to display in the templates."""

        return f'{self.riot_id} #{self.riot_tag}'
