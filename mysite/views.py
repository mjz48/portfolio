from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

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


def login_page(request):
    """ page for logging in to admin dashboard
    """
    if request.user.is_authenticated():
        return redirect('dashboard')

    if request.method == 'POST':
        if 'username' not in request.POST or 'password' not in request.POST:
            messages.add_message(request, messages.ERROR, 'Invalid credentials provided.')
            return redirect('index')

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid credentials provided.')
            return redirect('index')

    context = {
        'login_form': AuthenticationForm(),
        'wallpaper': Wallpaper.get_random_wallpaper(),
    }
    return render(request, 'login.html', context)