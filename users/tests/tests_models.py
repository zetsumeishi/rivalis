from django.test import TestCase

from users.tests.factories import UserFactory


class UsersModelsTests(TestCase):
    def setUp(self):
        self.player = UserFactory()

    def tests_user(self):
        self.assertEqual(self.player.__str__(), 'player0@rivalis.gg')
