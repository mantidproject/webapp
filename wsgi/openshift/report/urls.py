from django.conf.urls import patterns, url

from report import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^host/(?P<md5>\w+)?$', views.host, name='host'),
    url(r'^user/(?P<md5>\w+)?$', views.user, name='user'),
)
