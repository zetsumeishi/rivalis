from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory


class UsersViewsTests(TestCase):
    def setUp(self):
        self.player = UserFactory()
        self.player_to_delete = UserFactory()
        self.User = get_user_model()

    def tests_profile(self):
        url = reverse('users:profile')

        # [GET] AnonymousUser
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'],
            '/accounts/login/?next=/my-account/profile/',
        )

        # [GET] Authenticated User
        self.client.force_login(self.player)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, self.player.email)

        # [POST] Changing username and timezone
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
        self.assertFalse(response.context['teams'])
        self.assertFalse(response.context['organization'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Profile updated successfully')

        # [POST] Changing username without providing required fields
        payload = {'username': 'ioRek'}
        response = self.client.post(url, payload)
        messages = list(response.context['messages'])
        self.player.refresh_from_db()
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Mistakes were made')
        self.assertEqual(self.player.username, 'SpawN')

        self.client.logout()

    def tests_signup(self):
        url = reverse('users:signup')
        email = 'heaton@rivalis.gg'
        password = 'KQ3aiBM(=+9='
        timezone = 'Europe/Tallinn'
        username = 'HeatoN'

        # [GET] Render the signup form
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])

        # [POST] Create a user with username missing
        payload = {
            'email': email,
            'password1': password,
            'password2': password,
            'timezone': timezone,
        }
        response = self.client.post(url, payload, follow=True)
        with self.assertRaises(ObjectDoesNotExist):
            self.User.objects.get(email=email)

        # [POST] Create a valid user
        payload.update(username=username)
        response = self.client.post(url, payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.User.objects.get(email=email))

    def tests_delete_account(self):
        url = reverse('users:delete_account')

        # [GET] A user deletes his account and is redirected to the home page
        self.client.force_login(self.player_to_delete)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            self.player_to_delete.refresh_from_db()
