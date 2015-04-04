from django.shortcuts import render

from mysite.models import Wallpaper


def index(request):
    """ main site page
    """
    # get a random wallpaper
    wallpaper = Wallpaper.objects.all()[0]

    context = {
        'wallpaper': wallpaper,
    }
    return render(request, 'index.html', context)


def resume(request):
    """ page to see resume on site
    """
    context = {}
    return render(request, 'resume.html', context)