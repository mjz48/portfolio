from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'resume', views.resume, name='resume'),
)

# setup serving of media asserts on development environment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)