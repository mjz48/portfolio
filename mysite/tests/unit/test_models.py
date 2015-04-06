import os

from PIL import Image

from django.conf import settings
from django.core.files import File
from django.test.testcases import TestCase

from mysite.models import Wallpaper


class TestModels(TestCase):
    """ unit tests for Django models
    """

    ###########################################################################
    # Wallpaper model
    ###########################################################################
    def test_wallpaper_no_resize(self):
        """ make sure a wallpaper that is smaller than MAX_SIZE is not altered
            whatsoever
        """
        dummy_filename = 'test_img_3.jpg'
        dummy_root = os.path.join(settings.MEDIA_ROOT, Wallpaper.WALLPAPER_DIR)

        try:
            test_img_dir = os.path.join(settings.BASE_DIR, 'mysite', 'tests')

            orig_img = Image.open(open(os.path.join(test_img_dir, dummy_filename), 'rb'))
            orig_size = orig_img.size
            orig_img.close()

            w = Wallpaper()
            w.title = 'Test Image 3'
            w.author = 'Unknown'
            w.url.save(dummy_filename, File(open(os.path.join(test_img_dir, dummy_filename), 'rb')))
            w.save()

            test_img = Image.open(open(os.path.join(dummy_root, dummy_filename), 'rb'))
            resized_size = test_img.size
            test_img.close()

            self.assertLess(resized_size[0], Wallpaper.MAX_SIZE[0])
            self.assertLess(resized_size[1], Wallpaper.MAX_SIZE[1])
            self.assertEqual(orig_size[0], resized_size[0])
            self.assertEqual(orig_size[1], resized_size[1])
        finally:
            try:
                fn = w.url.name
                os.remove(os.path.join(settings.MEDIA_ROOT, fn))
            except OSError:
                pass

    def test_wallpaper_exact_no_resize(self):
        """ make sure a wallpaper that is the same size as MAX_SIZE is
            not resized at all
        """
        dummy_filename = 'test_img_1.jpg'
        dummy_root = os.path.join(settings.MEDIA_ROOT, Wallpaper.WALLPAPER_DIR)

        try:
            test_img_dir = os.path.join(settings.BASE_DIR, 'mysite', 'tests')

            orig_img = Image.open(open(os.path.join(test_img_dir, dummy_filename), 'rb'))
            orig_size = orig_img.size
            orig_img.close()

            w = Wallpaper()
            w.title = 'Test Image 1'
            w.author = 'Unknown'
            w.url.save(dummy_filename, File(open(os.path.join(test_img_dir, dummy_filename), 'rb')))
            w.save()

            test_img = Image.open(open(os.path.join(dummy_root, dummy_filename), 'rb'))
            resized_size = test_img.size
            test_img.close()

            self.assertEqual(resized_size[0], Wallpaper.MAX_SIZE[0])
            self.assertEqual(resized_size[1], Wallpaper.MAX_SIZE[1])
            self.assertEqual(orig_size[0], resized_size[0])
            self.assertEqual(orig_size[1], resized_size[1])
        finally:
            try:
                fn = w.url.name
                os.remove(os.path.join(settings.MEDIA_ROOT, fn))
            except OSError:
                pass

    def test_wallpaper_max_resize(self):
        """ make sure a wallpaper that is larger than the max size is
            resize to fit
        """
        dummy_filename = 'test_img_2.jpg'
        dummy_root = os.path.join(settings.MEDIA_ROOT, Wallpaper.WALLPAPER_DIR)

        try:
            test_img_dir = os.path.join(settings.BASE_DIR, 'mysite', 'tests')

            orig_img = Image.open(open(os.path.join(test_img_dir, dummy_filename), 'rb'))
            orig_size = orig_img.size
            orig_img.close()

            w = Wallpaper()
            w.title = 'Test Image 2'
            w.author = 'Unknown'
            w.url.save(dummy_filename, File(open(os.path.join(test_img_dir, dummy_filename), 'rb')))
            w.save()

            test_img = Image.open(open(os.path.join(dummy_root, dummy_filename), 'rb'))
            resized_size = test_img.size
            test_img.close()

            self.assertLessEqual(resized_size[0], Wallpaper.MAX_SIZE[0])
            self.assertLessEqual(resized_size[1], Wallpaper.MAX_SIZE[1])
            self.assertNotEqual(orig_size[0], resized_size[0])
            self.assertNotEqual(orig_size[1], resized_size[1])
        finally:
            try:
                fn = w.url.name
                os.remove(os.path.join(settings.MEDIA_ROOT, fn))
            except OSError:
                pass

    def test_wallpaper_optional_author(self):
        """ wallpapers should have authors, but sometimes, this field will
            be blank
        """
        dummy_filename = 'test_img_3.jpg'

        try:
            test_img_dir = os.path.join(settings.BASE_DIR, 'mysite', 'tests')

            w = Wallpaper()
            w.title = 'Test Image 3'
            w.url.save(dummy_filename, File(open(os.path.join(test_img_dir, dummy_filename), 'rb')))
            w.save()

            self.assertIsNone(w.author)
        finally:
            try:
                fn = w.url.name
                os.remove(os.path.join(settings.MEDIA_ROOT, fn))
            except OSError:
                pass

    def test_wallpaper_optional_title(self):
        """ wallpapers should have titles, but if there is none, it should
            automatically be called 'untitled'
        """
        dummy_filename = 'test_img_3.jpg'

        try:
            test_img_dir = os.path.join(settings.BASE_DIR, 'mysite', 'tests')

            w = Wallpaper()
            w.author = 'Unknown'
            w.url.save(dummy_filename, File(open(os.path.join(test_img_dir, dummy_filename), 'rb')))
            w.save()

            self.assertEquals('Untitled', w.title)
        finally:
            try:
                fn = w.url.name
                os.remove(os.path.join(settings.MEDIA_ROOT, fn))
            except OSError:
                pass

    def test_wallpaper_required_image(self):
        """ wallpapers need to have an associated image field value. If this
            is missing, expect an exception on save()
        """
        w = Wallpaper()
        w.author = 'Unknown'
        self.assertRaises(ValueError, w.save)

    def test_get_random_wallpaper1(self):
        """ create one wallpaper object and test the return random wallpaper
            function
        """
        w = Wallpaper()
        w.author = 'John Goodman'
        w.title = 'Call the Whambulance!'

        img_filename = 'test_img_2.jpg'
        file_path = os.path.join(settings.BASE_DIR, 'mysite', 'tests', img_filename)
        w.url.save(img_filename, File(open(file_path, 'rb')))
        w.save()

        received_w = Wallpaper.get_random_wallpaper()
        self.assertIsNotNone(received_w)
        self.assertEqual(received_w.id, w.id)

    def test_get_random_wallpaper2(self):
        """ create two wallpaper objects and test the return random wallpaper
            function
        """
        instances = {}
        for i in range(2):
            instances[i] = Wallpaper()
            instances[i].title = 'Random Wallpaper %d' % i
            instances[i].author = 'Author %d' % i

            path = os.path.join(settings.BASE_DIR, 'mysite', 'tests', 'test_img_%s.jpg' % (i + 1))
            instances[i].url.save(path, File(open(path, 'rb')))
            instances[i].save()

        received_w = Wallpaper.get_random_wallpaper()
        self.assertIsNotNone(received_w)

        ids = [w.id for w in instances.itervalues()]
        self.assertIn(received_w.id, ids)

    def test_get_random_wallpaper3(self):
        """ create three wallpaper objects and test the return random wallpaper
            function
        """
        instances = {}
        for i in range(3):
            instances[i] = Wallpaper()
            instances[i].title = 'Random Wallpaper %d' % i
            instances[i].author = 'Author %d' % i

            path = os.path.join(settings.BASE_DIR, 'mysite', 'tests', 'test_img_%s.jpg' % (i + 1))
            instances[i].url.save(path, File(open(path, 'rb')))
            instances[i].save()

        received_w = Wallpaper.get_random_wallpaper()
        self.assertIsNotNone(received_w)

        ids = [w.id for w in instances.itervalues()]
        self.assertIn(received_w.id, ids)

    def test_get_random_wallpaper_empty(self):
        """ the get random wallpaper class function should return NoneType
            when there are no object instances in the database
        """
        try:
            wallpaper = Wallpaper.get_random_wallpaper()
        except Exception as e:
            self.fail('Wallpaper.get_random_wallpaper: %s' % e.message)

        self.assertIsNone(wallpaper)