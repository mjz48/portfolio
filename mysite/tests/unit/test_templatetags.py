import os

from django.conf import settings
from django.core.files import File
from django.template import Template, Context
from django.test.testcases import TestCase

from mysite.models import Wallpaper


class TestTemplateTags(TestCase):
    """ unit tests for mysite template tags
    """
    files = []

    def setUp(self):
        try:
            w = Wallpaper()
            w.title = 'test wallpaper 1'
            w.author = 'test author'

            filename = 'test_img_1.jpg'
            path = os.path.join(settings.BASE_DIR, 'mysite', 'tests', filename)
            w.image.save(filename, File(open(path, 'rb')))
            w.save()
        finally:
            self.files.append(os.path.join(settings.MEDIA_ROOT, w.image.name))

    def tearDown(self):
        for f in self.files:
            try:
                os.remove(f)
            except OSError:
                pass

    def test_get_wallpaper(self):
        """ test get_wallpaper template tag
        """
        template = Template(
            """{% load mysite_tags %}
                {% get_wallpaper %}

                {% if wallpaper %}
                True
                {% else %}
                False
                {% endif %}
            """
        )
        rendered = template.render(Context({}))

        self.assertIn('True', rendered)