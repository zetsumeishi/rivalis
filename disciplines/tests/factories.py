import factory
from factory.django import DjangoModelFactory
from slugify import slugify

from disciplines.models import Discipline


class DisciplineFactory(DjangoModelFactory):
    class Meta:
        model = Discipline

    name = 'League of Legends'
    slug = factory.LazyAttribute(lambda n: slugify(n.name))
    short_name = 'LoL'
    editor_name = 'Riot Games'
    editor_website = 'https://www.riotgames.com/en'
