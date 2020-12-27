from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory


class UsersViewsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def tests_home(self):
        url = reverse('www:home')

        # [GET] Home as AnonymousUser
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # [GET] Home as User
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
