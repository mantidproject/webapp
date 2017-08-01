from django.shortcuts import render

# Create your views here.
from .models import Message, Usage, FeatureUsage, Location
from rest_framework import response, views, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .serializer import MessageSerializer, UsageSerializer, FeatureSerializer, LocationSerializer
import django_filters
from rest_framework import generics
from rest_framework.reverse import reverse
from django.http import HttpResponse
import json
import datetime
import hashlib
import settings
import json
import plots as lel

OS_NAMES = ['Linux', 'Windows NT', 'Darwin']
UTC = datetime.tzinfo('UTC')

def createLocation(ipAddress):
    if not settings.ON_OPENSHIFT and ipAddress == "127.0.0.1":
        ipAddress = "130.246.132.176"
        """ ipinfo's API has a bad JSON format for 127.0.0.1 requests.
        This changes the loopback IP to a random address for testing.
        Location should have IP as a unique field. Change the IP
        or you won't be able to add the test value more than once. """
    ipHash = hashlib.md5(ipAddress).hexdigest()
    if len(Location.objects.all().filter(ip=ipHash)) == 0:
        ''' check for the HASHED ip in the database. If it isn't present,
            create a new entry with the NON-HASHED ip as an argument. '''
        entity = Location()
        entity.create(ip=ipAddress)
    return ipHash

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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
            filter_lookups = {self.name: value}
            queryset = queryset.filter(**filter_lookups)
        return queryset


class UsageFilter(django_filters.FilterSet):
    date = WithinDateFilter(name="dateTime")
    datemin = django_filters.DateFilter(name="dateTime", lookup_expr='gte')
    datemax = django_filters.DateFilter(name="dateTime", lookup_expr='lt')
    uid = MD5Filter(name="uid")
    host = MD5Filter(name="host")
    ip = MD5Filter(name="ip")

    class Meta:
        model = Usage
        #fields = ['date', 'datemin','datemax', 'osName']
        fields = '__all__'
        order_by = ['-dateTime']


class UsageViewSet(viewsets.ModelViewSet):
    """All usages registered in the system. Valid filter parameters are:
    'host', 'uid', 'datemin', 'datemax', and 'date'.
    """
    queryset = Usage.objects.all()
    serializer_class = UsageSerializer
    permission_classes = [AllowAny]
    filter_class = UsageFilter

    def create(self, request):
        if request.method == 'POST':
            # print "Request", request.body
            post_data = json.loads(request.body)
            # on openshift REMOTE_ADDR points at the django server
            HttpIP = request.META.get('HTTP_X_FORWARDED_FOR',
                                      request.META['REMOTE_ADDR'])
            ipHash = createLocation(HttpIP)

            if "usages" in post_data.keys():
                for usage in post_data["usages"]:
                    self.saveUsage(usage, ipHash)
            else:
                self.saveUsage(post_data, ipHash)
            return HttpResponse(status=201)
        else:
            return HttpResponse("Please supply feature usage data as POST.")

    def saveUsage(self, usage, ipHash):
        ip = ipHash
        #count = usage["count"]
        osReadable = usage["osReadable"]
        application = usage["application"]
        component = usage.get("component", '')
        uid = usage["uid"]
        host = usage["host"]
        dateTime = usage["dateTime"]
        osName = usage["osName"]
        osArch = usage["osArch"]
        osVersion = usage["osVersion"]
        ParaView = usage["ParaView"]
        mantidVersion = usage["mantidVersion"]
        mantidSha1 = usage["mantidSha1"]
        obj, created = Usage.objects.get_or_create(osReadable=osReadable,
                                                   application=application,
                                                   component=component,
                                                   uid=uid, host=host,
                                                   dateTime=dateTime,
                                                   osName=osName,
                                                   osArch=osArch,
                                                   osVersion=osVersion,
                                                   ParaView=ParaView,
                                                   mantidVersion=mantidVersion,
                                                   mantidSha1=mantidSha1,
                                                   ip=ip)
                                                   #defaults={'count': 0})
        #obj.count += count
        obj.save()


def filterByDate(queryset, request=None, datemin=None, datemax=None):
    if request:
        datemin = request.GET.get("datemin", datemin)
        datemax = request.GET.get("datemax", datemax)
        # datemax = request.data.get("datemax", datemax)
        # datemax = request.data.get("datemax", datemax)

    if datemin:
        queryset = django_filters.DateFilter(
            name="dateTime", lookup_expr='gte').filter(queryset, datemin)

    if datemax:
        queryset = django_filters.DateFilter(
            name="dateTime", lookup_expr='lt').filter(queryset, datemax)

    return (queryset, datemin, datemax)


def parseDate(date):
    date = date.split('-')
    date = [int(i) for i in date]
    date = datetime.date(*date)
    return date


def getDateRange(queryset, datemin=None, datemax=None):
    queryset = queryset.order_by("dateTime")
    dates = []
    delta = datetime.timedelta(days=1)
    if datemin:
        item = parseDate(datemin)
    else:
        item = queryset.first().dateTime.date()
    if datemax:
        end = parseDate(datemax)
    else:
        end = queryset.last().dateTime.date()
    while item <= end:
        dates.append(item)
        item += delta
    return dates


def prepResult(dates):
    result = {'date': dates, 'total': [], 'other': []}
    for label in OS_NAMES:
        result[label] = []
    return result


def convertResult(result):
    mapping = {'Linux': 'linux', 'Darwin': 'mac', 'Windows NT': 'windows'}
    for key in mapping.keys():
        if key in result:
            result[mapping[key]] = result.pop(key)
    return result


@api_view(('GET',))
def host_list(request, format=None):
    """List of hosts. This can be filtered with 'datemin' and 'datemax' parameters"""
    queryset = Usage.objects.all()
    (queryset, datemin, datemax) = filterByDate(queryset, request)

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
    (queryset, datemin, datemax) = filterByDate(queryset, request)

    uids = []
    uid_names = []
    for uid in queryset.order_by("-dateTime")\
            .values('uid', 'dateTime'):
        if not uid['uid'] in uid_names:
            uid_names.append(uid['uid'])
            uids.append(uid)

    return response.Response(uids)


def query_count(queryset, field):
    if field:
        return queryset.order_by(field).values(field).distinct().count()
    else:
        return queryset.count()


def usage_by_field(request, format=None, field=None):
    (queryset, datemin, datemax) = filterByDate(Usage.objects.all(), request)
    dates = getDateRange(queryset, datemin, datemax)
    result = prepResult(dates)

    dateFilter = WithinDateFilter('dateTime')
    for date in dates:
        queryset_date = dateFilter.filter(queryset, date)
        total = query_count(queryset_date, field)
        cumulative = 0
        for label in OS_NAMES:
            count = query_count(queryset_date.filter(osName=label), field)
            cumulative += count
            result[label].append(count)
        result['total'].append(total)
        # one user can be on multiple systems
        result['other'].append(max(0, total - cumulative))

    result = convertResult(result)

    # make the result look like a d3.csv load
    finalResult = []
    for i in xrange(len(result['date'])):
        line = {}
        for key in result.keys():
            line[key] = result[key][i]
        finalResult.append(line)

    return response.Response(finalResult)


@api_view(('GET',))
def usage_by_hosts(request, format=None):
    return usage_by_field(request, format, 'host')


@api_view(('GET',))
def usage_by_users(request, format=None):
    return usage_by_field(request, format, 'uid')


@api_view(('GET',))
def usage_by_start(request, format=None):
    return usage_by_field(request, format)


@api_view(('GET',))
def api_root(request, format=None):
    return response.Response({
        'by':    reverse('by-root',    request=request, format=format),
        'host':  reverse('host-list',  request=request, format=format),
        'usage': reverse('usage-list', request=request, format=format),
        'user':  reverse('user-list',  request=request, format=format),
        'feature':  reverse('featureusage-list',  request=request, format=format),
        'location':  reverse('location-list',  request=request, format=format)
    })


@api_view(('GET',))
def by_root(request, format=None):
    return response.Response({
        'host': reverse('by-hosts', request=request, format=format),
        'user': reverse('by-users', request=request, format=format),
        'start': reverse('by-starts', request=request, format=format),
    })


class FeatureViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions,
    apart from create which has been extended to support a multi record format.
    """
    queryset = FeatureUsage.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny]

    # overridden create method, allows for normal rest signle record,
    # or a multi record json format, e.g.
    # {"features":[
    #   {"count":1,"internal":false,"name":"Load.v1","type":"Algorithm"},
    #   {"count":1,"internal":true,"name":"LoadInstrument.v1","type":"Algorithm"},
    #   {"count":1,"internal":true,"name":"LoadMuonLog.v1","type":"Algorithm"},
    #   {"count":1,"internal":true,"name":"LoadMuonNexus.v1","type":"Algorithm"}],
    # "mantidVersion":"3.5"}
    def create(self, request):
        if request.method == 'POST':
            # print "Request", request.body
            post_data = json.loads(request.body)
            version = post_data["mantidVersion"]
            if "features" in post_data.keys():
                for feature in post_data["features"]:
                    self.saveFeatureUsage(feature, version)
            else:
                self.saveFeatureUsage(post_data, version)
            return HttpResponse(status=201)
        else:
            return HttpResponse("Please supply feature usage data as POST.")

    def saveFeatureUsage(self, feature, version):
        count = feature["count"]
        internal = feature["internal"]
        type = feature["type"]
        name = feature["name"]
        obj, created = FeatureUsage.objects.get_or_create(name=name, type=type,
                                                          internal=internal,
                                                          mantidVersion=version,
                                                          defaults={'count': 0})
        obj.count += count
        obj.save()

def plots(request, md5):
    div = lel.barGraph()

    context = { "bar":div }
    return render(request, 'plots.html', context=context)

def year(request, md5, year):
    div2 = lel.pieChart(year)
    div3 = lel.mapGraph(year)
    context = { "pie":div2, "map":div3 }
    return render(request, 'plots.html', context=context)