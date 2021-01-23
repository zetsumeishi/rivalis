import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from slugify import slugify

from organizations.models import Organization
from organizations.models import Team
from organizations.models import TeamMembership
from users.tests.factories import UserFactory


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('company')
    slug = factory.LazyAttribute(lambda n: f'{slugify(n.name)}')
    short_name = factory.LazyAttribute(lambda n: f'{n.name[:3]}')
    description = fuzzy.FuzzyText(length=400)
    twitch = factory.LazyAttribute(lambda n: f'https://twitter.com/{slugify(n.name)}')
    owner = factory.SubFactory('users.tests.factories.UserFactory')


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    discipline = factory.SubFactory('disciplines.tests.factories.DisciplineFactory')
    organization = factory.SubFactory(
        OrganizationFactory,
    )
    name = factory.LazyAttribute(lambda n: f'{n.organization.name} {n.discipline.name}')
    slug = factory.LazyAttribute(lambda n: f'{slugify(n.name)}')

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of members were passed in, use them
            for member in extracted:
                self.members.add(member)


class TeamMembershipFactory(DjangoModelFactory):
    class Meta:
        model = TeamMembership

    id = factory.Sequence(lambda n: n)
    role = 'player'
    user = factory.SubFactory('users.tests.factories.UserFactory')
    team = factory.SubFactory('organizations.tests.factories.TeamFactory')


class UserWithTeamFactory(UserFactory):
    membership = factory.RelatedFactory(
        TeamMembershipFactory,
        factory_related_name='user',
    )
