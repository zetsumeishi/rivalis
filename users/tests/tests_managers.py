from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    """Tests for users.managers

    Custom managers to create a standard and superuser
    """

    def setUp(self):
        self.User = get_user_model()
        self.password = 'KQ3aiBM(=+9='

    def test_create_user(self):
        """Tests for users.managers.create_user"""

        email = 'user@rivalis.gg'

        # Creating a standard user with valid arguments
        user = self.User.objects.create_user(email=email, password=self.password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Creating a standard user without arguments
        with self.assertRaises(TypeError):
            self.User.objects.create_user()

        # Creating a standard user with just an email
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email=email)

        # Creating a standard user with an empty email
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', password=self.password)

    def test_create_superuser(self):
        """Tests for users.managers.create_superuser"""

        email = 'admin@rivalis.gg'

        # Creating a superuser with valid arguments
        admin_user = self.User.objects.create_superuser(email, self.password)

        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        # Creating a superuser passing is_superuser = False
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email=email,
                password=self.password,
                is_superuser=False,
            )

        # Creating a superuser passing is_staff = False
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email=email,
                password=self.password,
                is_superuser=True,
                is_staff=False,
            )
