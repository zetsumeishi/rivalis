from random import choice

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from faker import Faker

from tournaments.constants import REGION_CHOICES
from tournaments.models import Match
from tournaments.models import Round
from tournaments.models import Stage
from tournaments.models import Tournament
from tournaments.models import TournamentMembership

fake = Faker()


class TournamentFactory(DjangoModelFactory):
    class Meta:
        model = Tournament

    id = factory.Sequence(lambda n: n)
    description = fuzzy.FuzzyText(length=400)
    name = factory.LazyAttribute(lambda n: f'Rivalis Opens #{n.id}')
    prizes = fuzzy.FuzzyText(length=400)
    region = fuzzy.FuzzyChoice(REGION_CHOICES)
    rules = fuzzy.FuzzyText(length=400)
    size = 8

    # Relationships
    discipline = factory.SubFactory('disciplines.tests.factories.DisciplineFactory')
    organizer = factory.SubFactory('organizations.tests.factories.OrganizationFactory')
    participants = factory.SubFactory('organizations.tests.factories.TeamFactory')


class TournamentMembershipFactory(DjangoModelFactory):
    class Meta:
        model = TournamentMembership

    id = factory.Sequence(lambda n: n)
    team = factory.SubFactory('organizations.tests.factories.TeamFactory')
    tournament = factory.SubFactory(TournamentFactory)


class StageFactory(DjangoModelFactory):
    class Meta:
        model = Stage

    id = factory.Sequence(lambda n: n)
    format = 'Single Elimination'
    tournament = factory.SubFactory(TournamentFactory)


class RoundFactory(DjangoModelFactory):
    class Meta:
        model = Round

    id = factory.Sequence(lambda n: n)
    first_round = False
    number = 1
    name = f'Round of {2**number}'
    stage = factory.SubFactory(StageFactory)


class MatchFactory(DjangoModelFactory):
    class Meta:
        model = Match

    id = factory.Sequence(lambda n: n)
    home_score = choice(fuzzy.FuzzyInteger(0, 4))
    away_score = choice(fuzzy.FuzzyInteger(0, 4))

    # Relationships
    home_team = factory.SubFactory('organizations.tests.factories.TeamFactory')
    away_team = factory.SubFactory('organizations.tests.factories.TeamFactory')
    round = factory.SubFactory(RoundFactory)
