from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'portfolio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('siteapp.urls')),
)
