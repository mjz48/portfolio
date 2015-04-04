from django.test.testcases import TestCase

from mysite import models


class TestModels(TestCase):
    """ unit tests for Django models
    """

    def test_wallpaper(self):
        """
        """
        self.fail('To be implemented')

    def test_wallpaper_max_resize(self):
        """ make sure a wallpaper that is larger than the max size is
            resize to fit
        """
        self.fail('To be implemented')

    def test_wallpaper_optional_author(self):
        """ wallpapers should have authors, but sometimes, this field will
            be blank
        """
        self.fail('To be implemented')

    def test_wallpaper_optional_title(self):
        """ wallpapers should have titles, but if there is none, it should
            automatically be called 'untitled'
        """
        self.fail('To be implemented')
