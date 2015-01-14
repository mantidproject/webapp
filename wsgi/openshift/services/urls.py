from django.conf.urls import patterns, include, url

from services import views

from rest_framework import routers
from services import views

router = routers.DefaultRouter()
#router.register(r'message', MessageViewSet)
router.register(r'usage', views.UsageViewSet)
#router.register(r'hosts', ListHosts) # doesn't work

urlpatterns = patterns('',
    url(r'^$', views.api_root),
    url(r'^',include(router.urls)),
    url(r'^host/$', views.host_list, name='host-list'),
    url(r'^user/$', views.user_list, name='user-list'),
)
