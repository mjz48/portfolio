from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from mysite import views


class TestIndex(TestCase):
    """ unit tests related to index page
    """

    ###########################################################################
    # controller
    ###########################################################################
    def test_reverse(self):
        """ preserve named url value
        """
        self.assertEqual(reverse('index'), '/')

    def test_resolve(self):
        """ preserve url to view function mapping
        """
        self.assertEqual(views.index, resolve('/').func)

    ###########################################################################
    # view
    ###########################################################################
