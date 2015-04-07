from django.core.urlresolvers import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.test.testcases import TestCase


class TestViews(TestCase):
    """ unit tests for Django views
    """

    def setUp(self):
        """ create Client
        """
        self.client = Client()

    ###########################################################################
    # login view
    ###########################################################################
    def test_login_get(self):
        """ this view should return a valid html document with a login form
        """
        response = self.client.get(reverse('login'))
        self.assertIn(response.status_code, [200, 304])
        self.assertIn('login_form', response.context[-1])

    def test_login_post(self):
        """ this view should return index page redirect
        """
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_login_success(self):
        """ create a user, login with the correct credentials
            and see if the result is the response of the correct page
        """
        user = User.objects.create_user(
            username='testbot',
            email='testbot@test.com',
            password='test',
        )
        user.save()

        post_data = {
            'username': user.username,
            'password': 'test',
        }
        response = self.client.post(reverse('login'), post_data)

        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], user.id)

    def test_login_fail(self):
        """ create a user, login with the correct credentials
            and see if the result is the response of the correct view
        """
        user = User.objects.create_user(
            username='testbot2',
            email='testbot2@test.com',
            password='test',
        )
        user.save()

        post_data = {
            'username': user.username,
            'password': 'wrongpassword',
        }
        response = self.client.post(reverse('login'), post_data)

        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)