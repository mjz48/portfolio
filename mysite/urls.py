from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    # favicon
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),

    url(r'^$', views.index, name='index'),
    url(r'resume', views.resume, name='resume'),

    url(r'login', views.login_page, name='login'),
    url(r'logout', views.logout_page, name='logout'),

    url(r'dashboard', views.dashboard, name='dashboard'),

    url(r'^api/forms/wallpaper', views.FormWallpaper.as_view(), name='form-wallpaper'),
]

# setup serving of media asserts on development environment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
