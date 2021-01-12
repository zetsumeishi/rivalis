from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory


class UsersViewsTests(TestCase):
    """Tests for users.views"""

    def setUp(self):
        self.player = UserFactory(
            email='spawn@rivalis.gg',
            username='spawn',
            timezone='Europe/Tallinn',
        )
        self.player_to_delete = UserFactory()
        self.User = get_user_model()

    def tests_profile(self):
        """Tests for users.views.profile"""

        url = reverse('users:profile')

        # [GET] AnonymousUser
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/login/?next=/profile/')

        # [GET] Authenticated User
        self.client.force_login(self.player)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, self.player.email)

        # [POST] Changing the username and the timezone
        payload = {
            'email': self.player.email,
            'timezone': 'Europe/Stockholm',
            'username': 'SpawN',
        }
        response = self.client.post(url, payload)
        messages = list(response.context['messages'])
        self.player.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.player.username, 'SpawN')
        self.assertEqual(self.player.timezone, 'Europe/Stockholm')
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['user'], self.player)
        self.assertTrue(response.context['form'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Profile updated successfully')

        # [POST] Changing the username without providing the required fields
        payload = {'username': 'ioRek'}
        response = self.client.post(url, payload)
        messages = list(response.context['messages'])
        self.player.refresh_from_db()

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Mistakes were made')
        self.assertEqual(self.player.username, 'SpawN')

        self.client.logout()

    def tests_signup(self):
        """Tests for users.views.signup"""

        url = reverse('users:signup')
        email = 'heaton@rivalis.gg'
        password = 'KQ3aiBM(=+9='
        username = 'HeatoN'
        timezone = 'Europe/Stockholm'

        # [GET] Rendering the signup form
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])

        # [POST] Creating a user with empty username
        payload = {
            'email': email,
            'password1': password,
            'password2': password,
            'timezone': timezone,
        }
        response = self.client.post(url, payload, follow=True)
        with self.assertRaises(ObjectDoesNotExist):
            self.User.objects.get(email=email)

        # [POST] Creating a valid user
        payload.update(username=username)
        response = self.client.post(url, payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.User.objects.get(email=email))

    def tests_delete_account(self):
        """Tests for users.views.delete_account"""

        url = reverse('users:delete_account')

        # [GET] Deleting a user account
        self.client.force_login(self.player_to_delete)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            self.player_to_delete.refresh_from_db()
