from django.db import models


class Wallpaper(models.Model):
    """ A model that contains information about a wallpaper picture that
        will be displayed on the front page.
    """
    # model specific class constants
    MAX_SIZE = (1920, 1080)

    # fields
    title = models.CharField(max_length=250, default="Untitled")
    author = models.CharField(max_length=150, blank=True, null=True)
    url = models.URLField(blank=False, null=False)