import os
import io
import random

from PIL import Image

from django.db import models
from django.core.files.storage import default_storage


class Wallpaper(models.Model):
    """ A model that contains information about a wallpaper picture that
        will be displayed on the front page.
    """
    # model specific class constants
    MAX_SIZE = (1920, 1080)
    WALLPAPER_DIR = 'wallpapers'

    # fields
    title = models.CharField(max_length=250, default="Untitled")
    author = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(
        upload_to=WALLPAPER_DIR,
        blank=False,
        null=False,
    )
    link = models.URLField(blank=False, null=False)

    @classmethod
    def get_random_wallpaper(cls):
        """ return a handle to a random wallpaper instance
        """
        try:
            max_id = cls.objects.latest('id').id
        except Wallpaper.DoesNotExist:
            return None

        random_id = random.randint(0, max_id)
        result_set = cls.objects.filter(id__gte=random_id)

        if result_set:
            return result_set[0]
        return None

    def save(self):
        """ resize image on file upload if necessary
        """
        # make sure imagefield is not null
        if not self.image:
            raise ValueError('url field of Wallpaper is required!')

        super(Wallpaper, self).save()
        self.resize_image()

    def resize_image(self):
        """ make sure image is smaller than MAX_SIZE and if not, resize
            the image to make it fit inside MAX_SIZE
        """
        if not self.image.name:
            return

        img = Image.open(io.BytesIO(default_storage.open(self.image.name).read()))
        img_size = img.size

        (filename, ext) = os.path.splitext(self.image.name)
        ext = ext or 'jpeg'
        ext = ext.replace('.', '')
        if ext == 'jpg':
            ext = 'jpeg'

        if img_size[0] > self.MAX_SIZE[0] or img_size[1] > self.MAX_SIZE[1]:
            resize_ratio = max(float(self.MAX_SIZE[0]) / img_size[0],
                               float(self.MAX_SIZE[1]) / img_size[1])
            img_size = (int(img_size[0] * resize_ratio),
                        int(img_size[1] * resize_ratio))
            img = img.resize(size=img_size, resample=Image.LANCZOS)

            cropped_image = img.crop((0, 0, self.MAX_SIZE[0], self.MAX_SIZE[1]))

            # save image back to the same url
            out_img = io.BytesIO()
            cropped_image.save(out_img, ext)
            image_file = default_storage.open(self.image.name, 'wb')
            image_file.write(out_img.getvalue())
            image_file.close()

            # if we are on Amazon S3, set the content type
            try:
                pass
                # TODO: finish this
                #default_storage.connection
            except AttributeError:
                pass