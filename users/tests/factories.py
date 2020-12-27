import random

import factory.fuzzy
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker

from users.constants import TIMEZONES

fake = Faker()
timezones = [tz[0] for tz in TIMEZONES]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    id = factory.Sequence(lambda n: n)
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = fake.password(length=12)
    is_active = True
    date_joined = timezone.now()
    last_login = timezone.now()
    username = factory.Sequence(lambda n: f'player{n}')
    email = factory.Sequence(lambda n: f'player{n}@rivalis.gg')
    riot_id = username
    riot_tag = f'#{random.randint(100, 999)}'
    timezone = factory.fuzzy.FuzzyChoice(timezones)


class StaffFactory(UserFactory):
    is_staff = True


class AdminFactory(UserFactory):
    is_staff = True
    is_superuser = True
