from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from mysite import views


class TestUrls(TestCase):
    """ unit tests related to urls
    """

    def test_index_reverse(self):
        """ preserve named url value
        """
        self.assertEqual(reverse('index'), '/')

    def test_index_resolve(self):
        """ preserve url to view function mapping
        """
        self.assertEqual(views.index, resolve('/').func)