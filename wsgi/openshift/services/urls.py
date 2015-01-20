from django.conf.urls import patterns, include, url

from services import views

from rest_framework import routers
from services import views

router = routers.DefaultRouter(trailing_slash=False)
#router.register(r'message', MessageViewSet)
router.register(r'usage', views.UsageViewSet)
#router.register(r'hosts', ListHosts) # doesn't work

urlpatterns = patterns('',
    url(r'^$', views.api_root),
    url(r'^',include(router.urls)),
    url(r'^by/$', views.by_root, name='by-root'),
    url(r'^by/host/', views.usage_by_hosts,  name='by-hosts'),
    url(r'^by/start/', views.usage_by_start,  name='by-starts'),
    url(r'^by/user/', views.usage_by_users,  name='by-users'),
    url(r'^host/$', views.host_list, name='host-list'),
    url(r'^user/$', views.user_list, name='user-list'),
)
