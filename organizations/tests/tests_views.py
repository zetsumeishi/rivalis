from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from slugify import slugify

from organizations.models import Organization
from organizations.models import Team
from organizations.tests.factories import OrganizationFactory
from organizations.tests.factories import TeamFactory
from users.tests.factories import UserFactory


class OrganizationsViewsTests(TestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.organization = OrganizationFactory(owner=self.owner)
        self.team = TeamFactory(organization=self.organization)

    def tests_detail_organization(self):
        """Tests for organizations.views.detail_organization"""

        payload = {
            'organization_slug': self.organization.slug,
        }
        url = reverse('organizations:detail_organization', kwargs=payload)
        self.client.force_login(self.owner)

        # [GET] A single team page
        response = self.client.get(url, payload)

        self.assertEqual(response.status_code, 200)

    def tests_create_organization(self):
        """Tests for organizations.views.create_organization"""

        url = reverse('organizations:create_organization')
        self.client.force_login(self.owner)
        name = 'Rivalis'
        short_name = 'RIV'
        slug = slugify(name)
        description = 'Description of team Rivalis.'
        twitch = 'https://twitch.com'

        # [POST] Create an organization with an empty name
        payload = {
            'name': '',
            'short_name': short_name,
            'slug': slug,
            'description': description,
            'website': '',
            'twitch': twitch,
            'youtube': '',
            'twitter': '',
            'instagram': '',
            'reddit': '',
        }
        response = self.client.post(url, payload)

        with self.assertRaises(ObjectDoesNotExist):
            Organization.objects.get(slug=slug)
        self.assertEqual(response.status_code, 200)

        # [POST] Create a team with valid args
        payload.update(name=name)
        response = self.client.post(url, payload, follow=True)
        organization = response.context['organization']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(organization)
        self.assertEqual(organization.name, name)
        self.assertEqual(organization.short_name, short_name)
        self.assertEqual(organization.slug, slug)
        self.assertEqual(organization.twitch, twitch)
        self.assertEqual(organization.owner, self.owner)

    def tests_detail_team(self):
        """Tests for organizations.views.detail_team"""

        payload = {
            'organization_slug': self.organization.slug,
            'team_slug': self.team.slug,
        }
        url = reverse('organizations:detail_team', kwargs=payload)
        self.client.force_login(self.owner)

        # [GET] A single team page
        response = self.client.get(url, payload)

        self.assertEqual(response.status_code, 200)

    def tests_create_team(self):
        """Tests for organizations.views.create_team"""

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
        response = self.client.post(url, payload, follow=True)
        team = response.context['team']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(team)
        self.assertEqual(team.name, name)
        self.assertEqual(team.slug, slug)
        self.assertEqual(team.discipline.name, discipline)
        self.assertTrue(team.members.all().exists())

        self.client.logout()
