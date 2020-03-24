from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from django.views.generic.base import RedirectView

import report
import services

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('services.urls')),
    # should be in services/urls.py
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', report.views.index, name='index'),
    # url(r'^$', RedirectView.as_view(url='/usage/', permanent=True)),
    url(r'^host/(?P<md5>\w+)?$', report.views.host, name='host'),
    url(r'^user/(?P<md5>\w+)?$', report.views.user, name='user'),
    url(r'^usage/(?P<md5>\w+)?$', services.views.usage_plots, name='plots'),
    url(r'^usage/year/(?P<year>\d{4})(?P<md5>\w+)?$', services.views.usage_year, name='year'),
    url(r'^uid/(?P<md5>\w+)?$', services.views.uid_plots, name='plots'),
    url(r'^uid/year/(?P<year>\d{4})(?P<md5>\w+)?$', services.views.uid_year, name='year'),
]
