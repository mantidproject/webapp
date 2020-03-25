from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

from django.views.generic.base import RedirectView

import report
import services

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('services.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('', report.views.index, name='index'),
    path('', RedirectView.as_view(url='/usage/', permanent=True)),
    path('host/<hostid>/', report.views.host, name='host'),
    path('host/', report.views.host_list, name='host_list'),
    path('user/', report.views.user_list, name='user_list'),
    path('user/<userid>/', report.views.user, name='user'),
    path('usage/', services.views.usage_plots, name='plots'),
    path('usage/year/<int:year>', services.views.usage_year, name='year'),
    path('uid/', services.views.uid_plots, name='plots'),
    path('uid/year/<int:year>', services.views.uid_year, name='year'),
]
