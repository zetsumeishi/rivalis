from django.test import TestCase

from .templatetags.member_role import member_role
from .tests.factories import UserFactory
from organizations.models import TeamMembership
from organizations.tests.factories import TeamFactory


class UsersTemplatetagsTests(TestCase):
    """Tests for users.templatetags"""

    def setUp(self):
        # Creating 5 users
        members = [UserFactory() for _ in range(5)]

        # Creating a team with the 5 newly created users
        self.team = TeamFactory(members=members)

        # Give each member the player role
        for member in members:
            membership = TeamMembership.objects.get(user=member, team=self.team)
            membership.role = 'player'
            membership.save()

        self.member = members[0]

    def tests_member_role(self):
        """Tests for users.templatetags.member_role"""

        role = member_role(self.member, self.team)
        self.assertEqual(role, 'Player')
