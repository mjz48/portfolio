from django import forms

from mysite.models import Wallpaper


class WallpaperForm(forms.ModelForm):
    """ Wallpaper adding form
    """
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Untitled'
    }))

    class Meta:
        model = Wallpaper
        fields = ['title', 'author', 'image', 'link']