import random

import factory.fuzzy
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.constants import TIMEZONES

timezones = [tz[0] for tz in TIMEZONES]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    id = factory.Sequence(lambda n: n)
    is_active = True
    date_joined = timezone.now()
    last_login = timezone.now()
    username = factory.Faker('user_name')
    email = factory.Faker('ascii_safe_email')
    password = factory.Faker('password', length=12)
    riot_id = factory.LazyAttribute(lambda n: n.username)
    riot_tag = f'#{random.randint(100, 999)}'
    timezone = factory.fuzzy.FuzzyChoice(timezones)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class StaffFactory(UserFactory):
    is_staff = True


class AdminFactory(UserFactory):
    is_staff = True
    is_superuser = True
