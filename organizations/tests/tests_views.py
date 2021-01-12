from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from slugify import slugify

from disciplines.tests.factories import DisciplineFactory
from organizations.models import Team
from organizations.tests.factories import OrganizationFactory
from users.tests.factories import UserFactory


class OrganizationsViewsTests(TestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.discipline = DisciplineFactory()
        self.organization = OrganizationFactory(owner=self.owner)

    def tests_create_team(self):
        url = reverse('organizations:create_team')
        self.client.force_login(self.owner)
        name = 'Rivalis LoL'
        slug = slugify(name)
        discipline = 'League of Legends'

        # [POST] Create a team with empty name
        payload = {
            'name': '',
            'slug': slug,
            'organization': self.organization,
            'discipline': discipline,
        }
        response = self.client.post(url, payload)

        with self.assertRaises(ObjectDoesNotExist):
            Team.objects.get(slug=slug)
        self.assertEqual(response.status_code, 200)

        # [POST] Create a team with valid args
        payload.update(name=name)
        response = self.client.post(url, payload)
        team = Team.objects.get(slug=slug)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(team)
        self.assertEqual(team.name, name)
        self.assertEqual(team.slug, slug)

        self.client.logout()
