from django.shortcuts import render

from mysite.models import Wallpaper


def index(request):
    """ main site page
    """
    context = {
        'wallpaper': Wallpaper.get_random_wallpaper(),
    }
    return render(request, 'index.html', context)


def resume(request):
    """ page to see resume on site
    """
    context = {}
    return render(request, 'resume.html', context)