from django.shortcuts import render


def index(request):
    """ main site page
    """
    context = {}
    return render(request, 'index.html', context)


def resume(request):
    """ page to see resume on site
    """
    context = {}
    return render(request, 'resume.html', context)