from django.views.generic import View
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from mysite.models import Wallpaper
from mysite.forms import WallpaperForm


def index(request):
    """ main site page
    """
    context = {
    }
    return render(request, 'index.html', context)


def resume(request):
    """ page to see resume on site
    """
    context = {
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
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid credentials provided.')
            return redirect('index')

    context = {
        'login_form': AuthenticationForm(),
    }
    return render(request, 'login.html', context)


@login_required(login_url='index')
def logout_page(request):
    """ logout authenticated user
    """
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logged out.')
    return redirect('index')


@login_required(login_url='index')
def dashboard(request):
    """ user dashboard. Admin controls to add wallpapers and fiddle with
        resume settings
    """
    page = 1
    paginator = Paginator(Wallpaper.objects.all(), 60)
    try:
        if 'p' in request.GET:
            page = request.GET['p']

        wallpapers_on_page = paginator.page(page)
    except PageNotAnInteger:
        wallpapers_on_page = paginator.page(1)
    except EmptyPage:
        wallpapers_on_page = paginator.page(paginator.num_pages)

    context = {
        'title': 'Dashboard',
        'wallpaper_form': WallpaperForm(),
        'wallpapers': wallpapers_on_page,
        'w_page': paginator.page(page),
    }
    return render(request, 'dashboard.html', context)


class FormWallpaper(View):
    """ API endpoint for forms to manage Wallpaper
    """
    def dispatch(self, request, *args, **kwargs):
        """ custom routing function to allow for delete
            and post methods in class
        """
        if request.method == 'GET':
            return HttpResponseForbidden()
        elif request.method == 'POST':
            if 'delete_wallpaper' in request.POST:
                return self.delete(request)
            return self.post(request)

    def post(self, request):
        """ create a new Wallpaper
        """
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        request.POST = request.POST.copy()  # make POST data mutable

        wallpaper_form = WallpaperForm(request.POST, request.FILES)
        if wallpaper_form.is_valid():
            wallpaper = wallpaper_form.save()

            msg = "Successfully added new Wallpaper '%s'." % wallpaper.title
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            errors = {}
            for field in wallpaper_form:
                errors[field.name] = field.errors

            msg = "<br>".join([k + ": " + " ".join(v) for k, v in errors.items() if v])
            messages.add_message(request, messages.ERROR, msg)

        return redirect(request.META['HTTP_REFERER'])

    def delete(self, request):
        """ delete a Wallpaper
        """
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        if 'delete_wallpaper' not in request.POST:
            return redirect(request.META['HTTP_REFERER'])

        try:
            wallpaper = Wallpaper.objects.filter(id=request.POST['delete_wallpaper'])
            wallpaper.delete()
        except Wallpaper.DoesNotExist:
            msg = "Wallpaper id #%d does not exist." % request.POST['delete_wallpaper']
            messages.add_message(request, messages.ERROR, msg)

        return redirect(request.META['HTTP_REFERER'])