from django.conf.urls import include, url
from django.urls import path

from rest_framework import routers
from services import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'usage', views.UsageViewSet)
router.register(r'feature', views.FeatureViewSet)
router.register(r'location', views.LocationViewSet)
# router.register(r'hosts', ListHosts) # doesn't work

urlpatterns = [
    path('', views.api_root),
    path('by', views.by_root, name='by-root'),
    path('by/host', views.usage_by_hosts,  name='by-hosts'),
    path('by/start', views.usage_by_start,  name='by-starts'),
    path('by/user', views.usage_by_users,  name='by-users'),
    path('host', views.host_list, name='host-list'),
    path('user', views.user_list, name='user-list'),
    # url(r'feature', views.feature_usage, name='feature_usage'),
]

urlpatterns += router.urls
