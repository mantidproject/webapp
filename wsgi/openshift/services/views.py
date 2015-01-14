from django.shortcuts import render

# Create your views here.
from .models import Message, Usage
from rest_framework import response, views, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .serializer import MessageSerializer, UsageSerializer
import django_filters
from rest_framework import generics
from rest_framework.reverse import reverse
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
  """All usages registered in the system. Valid filter parameters are:
    'host', 'uid', 'datemin', 'datemax', and 'date'.
  """
  queryset = Usage.objects.all()
  serializer_class = UsageSerializer
  permission_classes = [AllowAny]
  filter_class=UsageFilter


def filterByDate(queryset, request):
    datemin = request.query_params.get("datemin", None)
    if datemin:
        queryset = django_filters.DateFilter(name="dateTime", lookup_type='gte').filter(queryset, datemin)

    datemax = request.query_params.get("datemax", None)
    if datemax:
        queryset = django_filters.DateFilter(name="dateTime", lookup_type='lt').filter(queryset, datemax)

    return queryset

@api_view(('GET',))
def host_list(request, format=None):
  """List of hosts. This can be filtered with 'datemin' and 'datemax' parameters"""
  queryset = Usage.objects.all()
  queryset = filterByDate(queryset, request)

  hosts = []
  host_names = []
  # only return the values that are actually used - sort by most recent first
  for host in queryset.order_by("-dateTime")\
         .values('host', 'osReadable', 'osName', 'osArch', 'osVersion', 'dateTime'):
      if not host['host'] in host_names:
          host_names.append(host['host'])
          hosts.append(host)

  return response.Response(hosts)

@api_view(('GET',))
def user_list(request, format=None):
    """List of users. This can be filtered with 'datemin' and 'datemax' parameters"""
    queryset = Usage.objects.all()
    queryset = filterByDate(queryset, request)

    uids = []
    uid_names = []
    for uid in queryset.order_by("-dateTime")\
          .values('uid', 'dateTime'):
        if not uid['uid'] in uid_names:
            uid_names.append(uid['uid'])
            uids.append(uid)

    return response.Response(uids)

@api_view(('GET',))
def api_root(request, format=None):
    return response.Response({
        'host': reverse('host-list', request=request, format=format),
        'usage': reverse('usage-list', request=request, format=format),
        'user': reverse('user-list', request=request, format=format)
    })
