import os
import io
import random

from PIL import Image

from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings
from django.dispatch.dispatcher import receiver
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
    link = models.URLField(max_length=1000, blank=False, null=False)

    @classmethod
    def get_random_wallpaper(cls):
        """ return a handle to a random wallpaper instance
        """
        try:
            return cls.objects.order_by('?')[0]
        except IndexError:
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
                # will throw AttributeError if not using S3
                using_s3 = default_storage.connection

                import boto
                boto_url = os.path.join(settings.MEDIA_DIR, self.image.name)

                content_type = 'image/jpeg'
                f, ext = os.path.splitext(self.image.name)[1]
                if ext == '.png':
                    content_type = 'image/png'

                key = boto.connect_s3().get_bucket(settings.AWS_STORAGE_BUCKET_NAME).lookup(boto_url)
                key.copy(key.bucket, key.name, preserve_acl=True,
                         metadata={'Content-Type': content_type})
            except AttributeError:
                pass


@receiver(post_delete, sender=Wallpaper)
def wallpaper_post_delete(sender, instance, **kwargs):
    """ remove file from imageField
    """
    if instance.image:
        instance.image.delete(False)