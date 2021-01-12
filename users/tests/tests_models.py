from django.test import TestCase

from users.tests.factories import UserFactory


class UsersModelsTests(TestCase):
    """Tests for users.models

    models:
        - User(AbstractUser)
    """

    def setUp(self):
        self.player = UserFactory(email='player@rivalis.gg')

    def tests_user_model(self):
        """Tests for users.models.User methods"""

        self.assertEqual(self.player.__str__(), 'player@rivalis.gg')
