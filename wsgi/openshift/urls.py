from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import report

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('services.urls')),
    url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')), # should be in services/urls.py
    url(r'^$', report.views.index, name='index'),
    url(r'^host/(?P<md5>\w+)?$', report.views.host, name='host'),
    url(r'^user/(?P<md5>\w+)?$', report.views.user, name='user'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + staticfiles_urlpatterns()
