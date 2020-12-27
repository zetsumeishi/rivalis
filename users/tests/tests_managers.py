from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.password = 'password'

    def test_create_user(self):
        email = 'user@rivalis.gg'
        user = self.User.objects.create_user(email=email, password=self.password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', password=self.password)

    def test_create_superuser(self):
        email = 'admin@rivalis.gg'
        admin_user = self.User.objects.create_superuser(email, self.password)
        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email=email,
                password=self.password,
                is_superuser=False,
            )
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email=email,
                password=self.password,
                is_superuser=True,
                is_staff=False,
            )
