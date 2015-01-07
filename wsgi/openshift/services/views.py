from django.shortcuts import render

# Create your views here.
from .models import Message, Usage
from rest_framework import response, views, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .serializer import MessageSerializer, UsageSerializer, HostListSerializer, UserListSerializer
import django_filters
from rest_framework import generics
import hashlib
import settings

class MessageViewSet(viewsets.ModelViewSet):
  queryset = Message.objects.all()
  serializer_class = MessageSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

class WithinDateFilter(django_filters.DateFilter):
    def filter(self, queryset, value):
        from datetime import timedelta
        if value:
            # date_value = value.replace(hour=0, minute=0, second=0)
            filter_lookups = {
                "%s__range" % (self.name, ): (
                    value,
                    value + timedelta(days=1),
                ),
            }
            queryset = queryset.filter(**filter_lookups)
        return queryset

class MD5Filter(django_filters.CharFilter):
    def filter(self, queryset, value):
        if value:
            if len(value) != 32:
                value = hashlib.md5(value).hexdigest()
            filter_lookups = { self.name: value }
            queryset = queryset.filter(**filter_lookups)
        return queryset

class UsageFilter(django_filters.FilterSet):
    date    = WithinDateFilter(name="dateTime")
    datemin = django_filters.DateFilter(name="dateTime", lookup_type='gte')
    datemax = django_filters.DateFilter(name="dateTime", lookup_type='lt')
    uid = MD5Filter(name="uid")
    host = MD5Filter(name="host")

    class Meta:
        model = Usage
        fields = ['date', 'datemin','datemax']
        order_by = ['-dateTime']

class UsageViewSet(viewsets.ModelViewSet):
  queryset = Usage.objects.all()
  serializer_class = UsageSerializer
  permission_classes = [AllowAny]
  filter_class=UsageFilter
  filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)

class ListHosts(generics.ListAPIView):
  model = Usage
  serializer_class = HostListSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

  def get_queryset(self):
      # sqllite does not supported this
      if False: #settings.ON_OPENSHIFT:
          return Usage.objects.order_by('host').distinct('host')
      else:
          # but it doesn't so do the work by hand
          hosts = []
          host_names = []
          # only return the values that are actually used - sort by most recent first
          for host in Usage.objects.order_by('-dateTime')\
                .values('host', 'osReadable', 'osName', 'osArch', 'osVersion'):
              if not host['host'] in host_names:
                  host_names.append(host['host'])
                  hosts.append(host)
          return hosts

class ListUsers(generics.ListAPIView):
  model = Usage
  serializer_class = UserListSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

  def get_queryset(self):
      # sqllite does not supported this
      if False: #settings.ON_OPENSHIFT:
          return Usage.objects.order_by('host').distinct('host')
      else:
          # but it doesn't so do the work by hand
          uids = []
          uid_names = []
          # only return the values that are actually used - sort by most recent first
          for uid in Usage.objects.order_by('-dateTime')\
                .values('uid', 'dateTime'):
              if not uid['uid'] in uid_names:
                  uid_names.append(uid['uid'])
                  uids.append(uid)
          return uids
