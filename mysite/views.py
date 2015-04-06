from django.shortcuts import render

from mysite.models import Wallpaper


def index(request):
    """ main site page
    """
    context = {
        'site_title': 'Isle of Zhu',
        'wallpaper': Wallpaper.get_random_wallpaper(),
    }
    return render(request, 'index.html', context)


def resume(request):
    """ page to see resume on site
    """
    context = {
        'wallpaper': Wallpaper.get_random_wallpaper(),
    }
    return render(request, 'resume.html', context)