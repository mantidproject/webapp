from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.models import User
from rest_framework import routers
from services.views import MessageViewSet, UsageViewSet

router = routers.DefaultRouter(trailing_slash=False)
#router.register(r'message', MessageViewSet)
router.register(r'usage', UsageViewSet)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include(router.urls)), # should be in services/urls.py
    url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')), # should be in services/urls.py
    url(r'^report/', include('report.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + staticfiles_urlpatterns()
