from models import Location, Usage
from django.db.models import Count
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
import django_filters
from collections import defaultdict
import math
import plotly
import plotly.offline as py
import plotly.graph_objs as go
import pandas
import datetime
import random

start = datetime.date(2014, 1, 1)
now = datetime.datetime.today()
years = range(start.year, now.year + 1)

# Colors
TOTAL_COLOR = 'rgb(200,200,200)'
WIN_COLOR = 'rgb(70,70,220)'
MAC_COLOR = 'rgb(190,200,250)'
RHEL_COLOR = 'rgb(200,80,80)'
UBUNTU_COLOR = 'rgb(250,160,100)'
OTHER_COLOR = 'rgb(130,130,150)'

special_locations = [
        {
            'Name': 'ORNL',
            'Lat': 35.9606,
            'Lon': -83.9206
        },

        {
            'Name': 'ESS',
            'Lat': 55.6667,
            'Lon': 12.5833
        },

        {
            'Name': 'RAL',
            'Lat': 51.7500,
            'Lon': -1.2500
        },

        {
            'Name': 'ILL',
            'Lat': 45.6601,
            'Lon': 4.6308
        },

        {
            'Name': 'HZB',
            'Lat': 52.5238,
            'Lon': 13.400
        },

        {
            'Name': 'MLZ',
            'Lat': 48.2500,
            'Lon': 11.6500
        },

        {
            'Name': 'NCNR',
            'Lat': 39.3288,
            'Lon': -76.5967
        },

        {
            'Name': 'BNL',
            'Lat': 40.8695,
            'Lon': -72.8868
        },

        {
            'Name': 'PSI',
            'Lat': 47.5606,
            'Lon': 8.2856
        },
    ]

#
# Utility functions
#
def countOS(usage_QuerySet):
    """ Given a QuerySet of usages, return counts of each OS's usage and a dict
        of unknown (other) systems. """
    WinTotal = 0
    MacTotal = 0
    RhelTotal = 0
    UbuntuTotal = 0
    OtherTotal = defaultdict(int)

    for obj in usage_QuerySet.iterator():
        os = determineOS(obj["osName"], obj["osReadable"])
        if os[0] == "Windows":
            # OS Type = Windows
            WinTotal += obj["usage_count"]
        elif os[0] == "Mac":
            # OS Type = Mac OS X
            MacTotal += obj["usage_count"]
        elif os[0] == "Linux":
            # OS Type = Linux
            # Divide by distro - RHEL, Ubuntu, and Other
            if os[1] == "Other":
                OtherTotal['blank'] += obj["usage_count"]
            elif os[1] == "Red Hat":
                RhelTotal += obj["usage_count"]
            elif os[1] == "Ubuntu":
                UbuntuTotal += obj["usage_count"]
            else:
                OtherTotal[os[1]] += obj["usage_count"]
        else:
            # Not Linux, Mac, or Windows? What sorcery is this?
            OtherTotal += obj["usage_count"]
    return WinTotal, MacTotal, RhelTotal, UbuntuTotal, OtherTotal

def countOSByUid(uid_QuerySet):
    """ Given a QuerySet of usages, return counts of each OS's usage as it
    matches to a UID and include a dict of unknown (other) systems.
    Example:
    - UID Bob uses RedHat 25 times and Windows 3 times.
    - UID Steve uses RedHat 2 times and macOS 5 times.
    - countOSByUid returns (WinTotal = 1, MacTotal = 1, RhelTotal = 2, ...)
    """

    WinTotal = 0
    MacTotal = 0
    RhelTotal = 0
    UbuntuTotal = 0
    OtherTotal = defaultdict(int)

    unique_pairs = set()
    for obj in uid_QuerySet: # .order_by("uid"):
        pair = (obj['uid'], determineOS(obj["osName"], obj["osReadable"]))
        unique_pairs.add(pair)

    for uid, os in unique_pairs:
        if os[0] == "Windows":
            # OS Type = Windows
            WinTotal += 1
        elif os[0] == "Mac":
            # OS Type = Mac OS X
            MacTotal += 1
        elif os[0] == "Linux":
            # OS Type = Linux
            # Divide by distro - RHEL, Ubuntu, and Other
            if os[1] == "Other":
                OtherTotal['blank'] += 1
            elif os[1] == "Red Hat":
                RhelTotal += 1
            elif os[1] == "Ubuntu":
                UbuntuTotal += 1
            else:
                OtherTotal[os[1]] += 1
        else:
            # Not Linux, Mac, or Windows? What sorcery is this?
            OtherTotal += 1
    return WinTotal, MacTotal, RhelTotal, UbuntuTotal, OtherTotal

def getRandomColor():
    return 'rgb(%s, %s, %s)' % (
        random.randint(100, 255),
        random.randint(100, 255),
        random.randint(100, 255))

#
# OS Determination
#
def determineOS(osName, osReadable):
    """ Return tuple of OS type "Windows" and version "Windows 7" """
    if osName == "Windows NT":
        return ("Windows", "")
    if osName == "Darwin":
        return ("Mac", "")
    if osName == "Linux":
        if osReadable == "" or osReadable == "Linux":
            return ("Linux", "Other")
        elif "Red Hat" in osReadable or "Scientific" in osReadable or "CentOS" in osReadable:
            return ("Linux", "Red Hat")
        elif "Ubuntu" in osReadable:
            return ("Linux", "Ubuntu")
        else:
            version = str(osReadable).split()[0]
            return ("Linux", version)
    else:
<<<<<<< HEAD
        return ["Unknown", ""]

=======
        return ("Unknown", "")
>>>>>>> 9c09a55627453ebb4932fcc6d8adfbc2aa444dcd
#
# Links
#
def yearLinks():
    links = "<div id='links'>Select a Specific Year:<br /><br />"
    for year in years:
        links += "<a href = 'year/" + \
            str(year) + "'> " + str(year) + "</a>"
    links += "</div><br />"
    return links

def utilLinks():
    links = """
    <p>Other Reports:
                <a href="/host/">list of hosts</a>
                and <a href="/user/">list of users</a>
            </p>

            <p>You can also go to
            <a href='/api'>api</a>, <a href="/admin">admin</a>,
            or <a href="/phpmyadmin">sql admin</a></p>
            """
    return links

#
# Graphs
#


## Generic
def barGraph(data):
    TotalTrace, WindowsTrace, MacTrace, RedHatTrace, UbuntuTrace, OtherTrace = data

    TotalTrace = go.Bar(
        x=years,
        y=Total,
        name="Total",
        marker=dict(
            color=TOTAL_COLOR,
        ),
    )

    WindowsTrace = go.Bar(
        x=years,
        y=Windows,
        name="Windows",
        marker=dict(
            color=WIN_COLOR,
        ),
    )
    MacTrace = go.Bar(
        x=years,
        y=Mac,
        name="MacOS",
        marker=dict(
            color=MAC_COLOR,
        ),
    )

    RedHatTrace = go.Bar(
        x=years,
        y=RHEL,
        name="Red Hat",
        marker=dict(
            color=RHEL_COLOR,
        ),
    )

    UbuntuTrace = go.Bar(
        x=years,
        y=Ubuntu,
        name="Ubuntu",
        marker=dict(
            color=UBUNTU_COLOR,
        ),
    )

    OtherTrace = go.Bar(
        x=years,
        y=Other,
        name="Other Linux",
        marker=dict(
            color=OTHER_COLOR,
        ),
    )

    data = [TotalTrace, WindowsTrace, MacTrace,
            RedHatTrace, UbuntuTrace, OtherTrace]
    layout = go.Layout(
        xaxis=dict(
            range=[start.year - 0.5, now.year + 0.5]  # custom x-axis scaling
        ),
        barmode='group',
        margin=go.Margin(
            l=50,
            r=0,
            b=30,
            t=30,
            pad=1
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    div = py.plot(fig, output_type='div', show_link=False)
    return div

def pieChart(data):
    pass

def mapGraph(data):
    pass

## Usages
def usages_barGraph():
    Windows, Mac, RHEL, Ubuntu, Other, Total = [], [], [], [], [], []

    for year in years:
        usages = Usage.objects.filter(dateTime__year=year).values('osName', 'osReadable') \
            .annotate(usage_count=Count('osName'))  # get OS's and counts
        WinTotal, MacTotal, UbuntuTotal, RhelTotal, OtherTotal = countOS(
            usages)
        Windows.append(WinTotal)
        Mac.append(MacTotal)
        RHEL.append(RhelTotal)
        Ubuntu.append(UbuntuTotal)
        Other.append(len(OtherTotal))
        Total.append(WinTotal + MacTotal + RhelTotal +
                     UbuntuTotal + len(OtherTotal))
    data = [WinTotal, MacTotal, RhelTotal, UbuntuTotal, len(OtherTotal)]
    return barGraph(data)

def usages_pieChart(year):
    labels = []
    values = []
    colors = []
    usages = Usage.objects.filter(dateTime__year=year).values('osName', 'osReadable') \
        .annotate(usage_count=Count('osName'))  # get OS's and counts
    if not usages:
        return "Error: No OS data for this year."

    WinTotal, MacTotal, RhelTotal, UbuntuTotal, OtherTotal = countOS(usages)

    if WinTotal > 0:
        labels.append("Windows")
        values.append(WinTotal)
        colors.append(WIN_COLOR)
    if MacTotal > 0:
        labels.append("MacOS")
        values.append(MacTotal)
        colors.append(MAC_COLOR)
    if RhelTotal > 0:
        labels.append("Red Hat")
        values.append(RhelTotal)
        colors.append(RHEL_COLOR)
    if UbuntuTotal > 0:
        labels.append("Ubuntu")
        values.append(UbuntuTotal)
        colors.append(UBUNTU_COLOR)
    if OtherTotal > 0:
        for OS in OtherTotal:
            if OS == "blank" or OS == 'Linux':
                labels.append("Other Linux")
            else:
                labels.append(OS)
            values.append(OtherTotal[OS])
            colors.append(getRandomColor())
    layout = go.Layout(
        margin=go.Margin(
            l=0,
            r=50,
            b=50,
            t=30,
            pad=1
        ),
    )
    trace = go.Pie(labels=labels, values=values, marker=dict(
        colors=colors), direction="counter-clockwise")
    fig = go.Figure(data=[trace], layout=layout)
    return py.plot(fig, output_type='div', show_link=False)


def usages_mapGraph(year):
    usages = Usage.objects.filter(dateTime__year=year).values('ip').exclude(ip='') \
        .annotate(usage_count=Count('ip'))  # get ip's and counts
    jsonData = []

    for obj in usages.iterator():
        if len(obj['ip']) == 0:
            continue
        count = obj['usage_count']
        try:
            loc = Location.objects.get(ip=obj['ip'])
        except ObjectDoesNotExist:
            # No match for given IP
            continue
        jsonData.append(
            {
                'Lat': float(loc.latitude),
                'Lon': float(loc.longitude),
                'Country': loc.country,
                'Region': loc.region,
                'Value': count,
                'Label': ''
            }
        )
    if len(jsonData) == 0:
        return "<div>No Location data for this year.</div>"
    # collect together things with the same lat/lon
    usage_locations = pandas.DataFrame(jsonData)
    usage_locations = usage_locations.groupby(['Lat', 'Lon', 'Country', 'Region', 'Label'])[
        'Value'].sum().reset_index()
    cases = []
    for _, row in usage_locations.iterrows():
        if (abs(row['Lat']) == 0.0 and abs(row['Lon']) == 0.0):
            # [0,0] is a throwaway coordinate
            continue
        for location in special_locations:
            if (abs(row['Lat'] - location['Lat']) <= .0002 and abs(row['Lon'] - location['Lon']) <= .0002):
                row['Label'] = location['Name']
                continue
        cases.append(
            go.Scattergeo(
                lat=[row['Lat']],
                lon=[row['Lon']],
                name='%d (%.4f, %.4f) - %s' % (row['Value'],
                                               row['Lat'], row['Lon'], row['Region']),
                text=row['Label'],
                marker=dict(
                    size=5 * math.log(row['Value'] + 1),
                    color='rgba(255,90,90,0.6)',
                    line=dict(width=0)
                ),
                mode='markers+text',
                textposition='bottom center',
                showlegend=False,
                hoverinfo="name",
                hoverlabel=dict(
                    namelength=[-1]
                )
            )
        )
    layout = go.Layout(
        title='Location Data',
        geo=dict(
            showframe=True,
            showcoastlines=True,
            showcountries=True,
            showland=True,
            showsubunits=True,
            landcolor="rgb(229, 229, 229)",
            countrycolor="rgb(255, 255, 255)",
            coastlinecolor="rgb(255, 255, 255)",
            subunitcolor="rgb(255, 255, 255)",
            projection=dict(
                type='Mercator'
            ),
            lonaxis=dict(range=[-150.0, 150.0]),
            lataxis=dict(range=[-100.0, 100.0]),
            domain=dict(
                x=[0, 1],
                y=[0, 1]
            )
        ),
        margin=go.Margin(
            l=20,
            r=20,
            b=10,
            t=30,
            pad=1
        ),

        # Put newer and larger circles at the z-bottom so the old ones show up
    )
    fig = go.Figure(layout=layout, data=cases)
    div = py.plot(fig, validate=False, output_type='div', show_link=False)
    return div


## Uids
def uids_barGraph():
    Windows, Mac, RHEL, Ubuntu, Other, Total = [], [], [], [], [], []

    for year in years:
        uids = Usage.objects.filter(dateTime__year=year) \
                .values('osName', 'osReadable', 'uid')
        WinTotal, MacTotal, UbuntuTotal, RhelTotal, OtherTotal = countOSByUid(uids)
        Windows.append(WinTotal)
        Mac.append(MacTotal)
        RHEL.append(RhelTotal)
        Ubuntu.append(UbuntuTotal)
        Other.append(len(OtherTotal))
        Total.append(WinTotal + MacTotal + RhelTotal +
                     UbuntuTotal + len(OtherTotal))
    data = [WinTotal, MacTotal, RhelTotal, UbuntuTotal, len(OtherTotal)]
    return barGraph(data)

def uids_pieChart(year):
    queryset = Usage.objects.filter(dateTime__year=year).values(
        'osName', 'osReadable', 'uid')
    if not queryset:
        return "Error: No user data for this year."

    unique_pairs = set()
    for obj in queryset:
        pair = (obj["uid"], determineOS(obj["osName"], obj["osReadable"]))
        unique_pairs.add(pair)

    WinTotal = 0
    MacTotal = 0
    RhelTotal = 0
    UbuntuTotal = 0
    OtherTotal = {}
    for uid, os in unique_pairs:
        if os[0] == "Windows":
            # OS Type = Windows
            WinTotal += 1
        elif os[0] == "Mac":
            # OS Type = Mac OS X
            MacTotal += 1
        elif os[0] == "Linux":
            # OS Type = Linux
            # Divide by distro - RHEL, Ubuntu, and Other
            if os[1] == "Other":
                if OtherTotal.has_key("blank"):
                    OtherTotal['blank'] += 1
                else:
                    OtherTotal['blank'] = 1
            elif os[1] == "Red Hat":
                RhelTotal += 1
            elif os[1] == "Ubuntu":
                UbuntuTotal += 1
            else:
                if OtherTotal.has_key(os[1]):
                    OtherTotal[os[1]] += 1
                else:
                    OtherTotal[os[1]] = 1
        else:
            # Not Linux, Mac, or Windows? What sorcery is this?
            OtherTotal += 1
    labels = []
    values = []
    colors = []

    if WinTotal > 0:
        labels.append("Windows")
        values.append(WinTotal)
        colors.append(WIN_COLOR)
    if MacTotal > 0:
        labels.append("MacOS")
        values.append(MacTotal)
        colors.append(MAC_COLOR)
    if RhelTotal > 0:
        labels.append("Red Hat")
        values.append(RhelTotal)
        colors.append(RHEL_COLOR)
    if UbuntuTotal > 0:
        labels.append("Ubuntu")
        values.append(UbuntuTotal)
        colors.append(UBUNTU_COLOR)
    if OtherTotal > 0:
        for OS in OtherTotal:
            if OS == "blank" or OS == 'Linux':
                labels.append("Other Linux")
            else:
                labels.append(OS)
            values.append(OtherTotal[OS])
            colors.append(getRandomColor())

    layout = go.Layout(
        margin=go.Margin(
            l=0,
            r=50,
            b=50,
            t=30,
            pad=1
        ),
    )
    trace = go.Pie(labels=labels, values=values, marker=dict(
        colors=colors), direction="counter-clockwise")
    fig = go.Figure(data=[trace], layout=layout)
    return py.plot(fig, output_type='div', show_link=False)

def uids_mapGraph(year):
    uids = Usage.objects.filter(dateTime__year=year).values('uid', 'ip')
    if not uids:
        return "<div>No location data for this year.</div>"
    jsonData = []
<<<<<<< HEAD
    unique_pairs = []
    for obj in uids.order_by("uid"):
        pair = {"uid":obj["uid"], "ip":obj["ip"]}
        if pair in unique_pairs:
            pass
        else:
            print pair
            unique_pairs.append(pair)
    for obj in unique_pairs:
=======

    unique_pairs = set()
    for obj in uids:
>>>>>>> 9c09a55627453ebb4932fcc6d8adfbc2aa444dcd
        if len(obj["ip"]) == 0:
            continue
        pair = (obj["uid"], obj["ip"])
        unique_pairs.add(pair)

    for uid, ip in unique_pairs:
        count = 1 #, I guess?
        try:
            loc = Location.objects.get(ip=ip)
        except ObjectDoesNotExist:
            # No match for given IP
            continue
        # only show one digit for location
        name = '(%.1f, %.1f) - %s' % (float(loc.latitude), float(loc.longitude), loc.region)
        jsonData.append(
            {
                'Lat': float(loc.latitude),
                'Lon': float(loc.longitude),
                'Country': loc.country,
                'Region': loc.region,
                'Name':name,
                'Value':count,
                'Label':''
            }
        )
    if len(jsonData) == 0:
        return "<div>No Location data for this year.</div>"
    # collect together things with the same lat/lon
    # see http://www.longitudestore.com/how-big-is-one-gps-degree.html
    # for justification of 2 decimal digits being plenty
    usage_locations = pandas.DataFrame(jsonData)
    usage_locations[['Lat','Lon']] = usage_locations[['Lat','Lon']].apply(lambda x: pandas.Series.round(x, 2))
    usage_locations = usage_locations.groupby(['Lat', 'Lon', 'Name', 'Label'])['Value'].sum().reset_index()
    cases = []
    for _, row in usage_locations.iterrows():
        if (abs(row['Lat']) == 0.0 and abs(row['Lon']) == 0.0):
            # [0,0] is a throwaway coordinate
            continue
        for location in special_locations:
            if (abs(row['Lat'] - location['Lat']) <= .01 and abs(row['Lon'] - location['Lon']) <= .01):
                row['Label'] = location['Name']
                oldlabel = row['Name'].split('- ')[-1]
                row['Name'] = row['Name'].replace(oldlabel, location['Name'])
                continue
        cases.append(
            go.Scattergeo(
                lat=[row['Lat']],
                lon=[row['Lon']],
                name='%d %s' % (row['Value'], row['Name']),
                text=row['Label'],
                marker=dict(
                    size=5 * math.log(row['Value'] + 1),
                    color='rgba(255,90,90,0.6)',
                    line=dict(width=0)
                ),
                mode='markers+text',
                textposition='bottom center',
                showlegend=False,
                hoverinfo="name",
                hoverlabel=dict(
                    namelength=[-1]
                )
            )
        )
    layout = go.Layout(
        title='Location Data',
        geo=dict(
            showframe=True,
            showcoastlines=True,
            showcountries=True,
            showland=True,
            showsubunits=True,
            landcolor="rgb(229, 229, 229)",
            countrycolor="rgb(255, 255, 255)",
            coastlinecolor="rgb(255, 255, 255)",
            subunitcolor="rgb(255, 255, 255)",
            projection=dict(
                type='Mercator'
            ),
            lonaxis=dict(range=[-150.0, 150.0]),
            lataxis=dict(range=[-100.0, 100.0]),
            domain=dict(
                x=[0, 1],
                y=[0, 1]
            )
        ),
        margin=go.Margin(
            l=20,
            r=20,
            b=10,
            t=30,
            pad=1
        ),

        # Put newer and larger circles at the z-bottom so the old ones show up
    )
    fig = go.Figure(layout=layout, data=cases)
    div = py.plot(fig, validate=False, output_type='div', show_link=False)
    return div

