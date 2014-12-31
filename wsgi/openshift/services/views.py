from django.shortcuts import render

# Create your views here.
from .models import Message, Usage
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .serializer import MessageSerializer, UsageSerializer
import django_filters

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

class UsageFilter(django_filters.FilterSet):
    date    = WithinDateFilter(name="dateTime")
    datemin = django_filters.DateFilter(name="dateTime", lookup_type='gte')
    datemax = django_filters.DateFilter(name="dateTime", lookup_type='lt')

    class Meta:
        model = Usage
        fields = ['date', 'datemin','datemax', 'host', 'uid']
        order_by = ['-dateTime']

class UsageViewSet(viewsets.ModelViewSet):
  queryset = Usage.objects.all()
  serializer_class = UsageSerializer
  permission_classes = [AllowAny]
  filter_class=UsageFilter
  filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
