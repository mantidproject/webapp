from models import Location, Usage
from django.db.models import Count
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
import django_filters
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


def getRandomColor():
    return 'rgb(%s, %s, %s)' % (
        random.randint(100, 255),
        random.randint(100, 255),
        random.randint(100, 255))


def barGraph():
    Windows, Mac, RHEL, Ubuntu, Other, Total = [], [], [], [], [], []

    for year in years:
        usages = Usage.objects.filter(dateTime__year=year).values('osName', 'osReadable') \
            .annotate(usage_count=Count('osName'))  # get OS's and counts
        WinTotal = 0
        MacTotal = 0
        RhelTotal = 0
        UbuntuTotal = 0
        OtherTotal = 0
        for obj in usages.iterator():
            name = obj["osName"]
            version = obj["osReadable"]
            if name == "Windows NT":
                # OS Type = Windows
                WinTotal += obj["usage_count"]
            elif name == "Darwin":
                # OS Type = Mac OS X
                MacTotal += obj["usage_count"]
            elif name == "Linux":
                # OS Type = Linux
                # Divide by distro - RHEL, Ubuntu, and Other
                if version == "":
                    OtherTotal += obj["usage_count"]
                elif "Red Hat" in version or "Scientific" in version or "CentOS" in version:
                    RhelTotal += obj["usage_count"]
                elif "Ubuntu" in version:
                    UbuntuTotal += obj["usage_count"]
                else:
                    OtherTotal += obj["usage_count"]
            else:
                # Not Linux, Mac, or Windows? What sorcery is this?
                OtherTotal += obj["usage_count"]
        Windows.append(WinTotal)
        Mac.append(MacTotal)
        RHEL.append(RhelTotal)
        Ubuntu.append(UbuntuTotal)
        Other.append(OtherTotal)
        Total.append(WinTotal + MacTotal + RhelTotal +
                     UbuntuTotal + OtherTotal)

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
        name="macOS",
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


def links():
    links = "<div id='links'>Select a Specific Year:<br /><br />"
    for year in years:
        links += "<a href = '/plots/year/" + \
            str(year) + "'> " + str(year) + "</a>"
    links += "</div><br />"
    return links


def pieChart(year):
    labels = []
    values = []
    colors = []
    usages = Usage.objects.filter(dateTime__year=year).values('osName', 'osReadable') \
        .annotate(usage_count=Count('osName'))  # get OS's and counts
    if not usages:
        return "Error: No OS data for this year."

    WinTotal = 0
    MacTotal = 0
    RhelTotal = 0
    UbuntuTotal = 0
    OtherTotal = {}

    for obj in usages.iterator():
        name = obj["osName"]
        version = obj["osReadable"]
        if name == "Windows NT":
            # OS Type = Windows
            WinTotal += obj["usage_count"]
        elif name == "Darwin":
            # OS Type = Mac OS X
            MacTotal += obj["usage_count"]
        elif name == "Linux":
            # OS Type = Linux
            # Divide by distro - RHEL, Ubuntu, and Other
            if version == "" or version == "Linux":
                if OtherTotal.has_key("blank"):
                    OtherTotal['blank'] += obj["usage_count"]
                else:
                    OtherTotal['blank'] = obj["usage_count"]
            elif "Red Hat" in version or "Scientific" in version or "CentOS" in version:
                RhelTotal += obj["usage_count"]
            elif "Ubuntu" in version:
                UbuntuTotal += obj["usage_count"]
            else:
                v = str(version).split()[0]
                if OtherTotal.has_key(v):
                    OtherTotal[v] += obj["usage_count"]
                else:
                    OtherTotal[v] = obj["usage_count"]
        else:
            # Not Linux, Mac, or Windows? What sorcery is this?
            OtherTotal += obj["usage_count"]

    if WinTotal > 0:
        labels.append("Windows")
        values.append(WinTotal)
        colors.append(WIN_COLOR)
    if MacTotal > 0:
        labels.append("macOS")
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


def mapGraph(year):
    special_locations = [
        { 
            'Name':'ORNL',
            'Lat':35.9606,
            'Lon':-83.9206 
        },

        { 
            'Name':'ESS',
            'Lat':-55.6667,
            'Lon':12.5833
        },

        { 
            'Name':'ISIS',
            'Lat':51.7500,
            'Lon':-1.2500
        },
    ]
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
                'Lat':float(loc.latitude),
                'Lon':float(loc.longitude),
                'Country':loc.country,
                'Region':loc.region,
                'Value':count*100,
                'Label':''
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
        print row
        if (abs(row['Lat']) == 0.0 and abs(row['Lon']) == 0.0):
            # [0,0] is a throwaway coordinate
            continue
        for location in special_locations:
            if (row['Lat'] == location['Lat'] and row['Lon'] == location['Lon']):
                row['Label'] = location['Name']
                continue
        cases.append(
            go.Scattergeo(
                lat=[row['Lat']],
                lon=[row['Lon']],
                name='%s, %s' % (row['Region'], row['Country']),
                text=row['Label'],
                marker=dict(
                    size= row['Value']/10000.0,
                    color='rgba(255,90,90,0.6)',
                    line=dict(width=0)
                ),
                mode='markers+text',
                textposition='bottom center'
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
        legend=dict()
        # Put newer and larger circles at the z-bottom so the old ones show up
    )
    fig = go.Figure(layout=layout, data=cases)
    div = py.plot(fig, validate=False, output_type='div', show_link=False)
    return div
