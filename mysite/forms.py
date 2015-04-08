from django import forms

from mysite.models import Wallpaper


class WallpaperForm(forms.ModelForm):
    """ Wallpaper adding form
    """
    class Meta:
        model = Wallpaper
        fields = ['title', 'author', 'image', 'link']