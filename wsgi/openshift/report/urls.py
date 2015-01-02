from django.conf.urls import patterns, url

from report import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^host/(?P<md5>\w+)$', views.host, name='index'),
    url(r'^uid/(?P<md5>\w+)$', views.uid, name='index'),
)