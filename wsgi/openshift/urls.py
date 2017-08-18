from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import report, services

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('services.urls')),
    # should be in services/urls.py
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', report.views.index, name='index'),
    url(r'^host/(?P<md5>\w+)?$', report.views.host, name='host'),
    url(r'^user/(?P<md5>\w+)?$', report.views.user, name='user'),
    url(r'^usage/(?P<md5>\w+)?$', services.views.usage_plots, name='plots'),
    url(r'^usage/year/(?P<year>\d{4})(?P<md5>\w+)?$', services.views.uid_year, name='year'),
    url(r'^uid/(?P<md5>\w+)?$', services.views.usage_plots, name='plots'),
    url(r'^uid/year/(?P<year>\d{4})(?P<md5>\w+)?$', services.views.uid_year, name='year'),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
