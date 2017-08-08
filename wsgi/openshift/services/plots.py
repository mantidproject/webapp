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
import time
import random

OS_LIST = ["Windows", "Mac", "RHEL", "Ubuntu", "Other"]
# RHEL or Red Hat or RedHat? Which is better for the project?
start = datetime.date(2014,1,1)
now = datetime.datetime.today()
years = range(start.year, now.year+1)

# Fake data for testing
all_time_data = {
    "2006": {
        "Windows": 20, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2007": {
        "Windows": 50, "Mac": 20, "RHEL": 90, "Ubuntu": 62, "Other": 10
    },
    "2008": {
        "Windows": 30, "Mac": 10, "RHEL": 90, "Ubuntu": 62, "Other": 10
    },
    "2009": {
        "Windows": 12, "Mac": 20, "RHEL": 80, "Ubuntu": 62, "Other": 10
    },
    "2010": {
        "Windows": 29, "Mac": 20, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2011": {
        "Windows": 56, "Mac": 40, "RHEL": 75, "Ubuntu": 62, "Other": 10
    },
    "2012": {
        "Windows": 41, "Mac": 41, "RHEL": 78, "Ubuntu": 62, "Other": 10
    },
    "2013": {
        "Windows": 55, "Mac": 31, "RHEL": 99, "Ubuntu": 62, "Other": 10
    },
    "2014": {
        "Windows": 54, "Mac": 22, "RHEL": 86, "Ubuntu": 62, "Other": 10
    },
    "2015": {
        "Windows": 55, "Mac": 15, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2016": {
        "Windows": 30, "Mac": 19, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2017": {
        "Windows": 92, "Mac": 45, "RHEL": 80, "Ubuntu": 72, "Other": 20
    }
}
# Let's just work with this as a given.
# It is here to find a good format to create either a new DB table/model, or
# to use caching to store these values locally.

# Colors
TOTAL_COLOR = 'rgb(200,200,200)'
WIN_COLOR = 'rgb(70,70,220)'
MAC_COLOR = 'rgb(190,200,250)'
RHEL_COLOR = 'rgb(200,80,80)'
UBUNTU_COLOR = 'rgb(250,160,100)'
OTHER_COLOR = 'rgb(130,130,150)'

def barGraph():
    Windows, Mac, RHEL, Ubuntu, Other, Total = [], [], [], [], [], []

    for year in years:
        usages = Usage.objects.filter(dateTime__year=year).values('osName', 'osReadable') \
        .annotate(usage_count=Count('osName')) #get OS's and counts
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
                elif "Red Hat Enterprise" in version:
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
        Total.append(WinTotal + MacTotal + RhelTotal + UbuntuTotal + OtherTotal)
    """
    for year in all_time_data:
        year_total = 0
        Windows.append(all_time_data[year]["Windows"])
        Mac.append(all_time_data[year]["Mac"])
        RHEL.append(all_time_data[year]["RHEL"])
        Ubuntu.append(all_time_data[year]["Ubuntu"])
        Other.append(all_time_data[year]["Other"])
        Total.append(sum(all_time_data[year].values()))
    # There must be a more compact way to do this.
    # FOR loop iterating over OS_LIST, maybe.
    """

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
        name="Red Hat Enterprise Linux",
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
            range=[start.year-0.5, now.year+0.5] # custom x-axis scaling
        ),
        barmode='group',
        width=750,
        height=600,
        margin=go.Margin(
            l=50,
            r=0,
            b=30,
            t=5,
            pad=1
        ), 
    )
    fig = go.Figure(data=data, layout=layout)
    div = py.plot(fig, output_type='div', show_link=False)
    return div

def links():
    links = "<div id='links'>Select a Specific Year:<br /><br />"
    for year in years:
        links += "<a href = '/plots/year/"+str(year)+"'> "+str(year)+"</a>"
    links += "</div><br />"
    return links

def pieChart(year):
    labels = []
    values = []
    colors = []
    """
    for os in OS_LIST:
        labels.append(os)
        values.append(all_time_data[year][os])
    """
    usages = Usage.objects.filter(dateTime__year=year).values('osName', 'osReadable') \
        .annotate(usage_count=Count('osName')) #get OS's and counts
    if not usages:
        return "Error: No OS data for this year."
    for obj in usages.iterator():
        name = obj["osName"]
        version = obj["osReadable"]
        
        if name == "Windows NT":
            # OS Type = Windows
            """
            if version == "":
                labels.append("Windows (Unknown Version)")
            elif "Server" in version:
                labels.append("Windows Server")
            elif "Windows 7" in version:
                labels.append("Windows 7")
            elif "Windows 8" in version:
                labels.append("Windows 8")
            elif "Windows 10" in version:
                labels.append("Windows 10")
            """
            labels.append("Windows")
            colors.append(WIN_COLOR)
        elif name == "Darwin":
            # OS Type = Mac OS X
            labels.append("macOS")
            colors.append(MAC_COLOR)
        elif name == "Linux":
            # OS Type = Linux
            # Divide by distro - RHEL, Ubuntu, and Other
            if version == "":
                labels.append("Linux (Unknown Distro)")
                colors.append(OTHER_COLOR)
            elif "Red Hat Enterprise" in version or "Scientific" in version:
                labels.append("Red Hat Enterprise Linux")
                colors.append(RHEL_COLOR)
            elif "Ubuntu" in version:
                labels.append("Ubuntu")
                colors.append(UBUNTU_COLOR)
            else:
                pretty_name = version.split()[0]
                if pretty_name == "Linux":
                    labels.append("Linux (Unknown Distro)")
                else:
                    labels.append(pretty_name)
                colors.append('rgb(%s, %s, %s)' % (
                    random.randint(100,255),
                    random.randint(100,255),
                    random.randint(100,255)
                    ) 
                )
        else:
            labels.append("Other (%s)" % name + version)
            colors.append(OTHER_COLOR)
        values.append(obj["usage_count"])

    #colors = [WIN_COLOR, MAC_COLOR, RHEL_COLOR, UBUNTU_COLOR, OTHER_COLOR]
    layout = go.Layout(
        width=500,
        height=500,
        margin=go.Margin(
            l=0,
            r=50,
            b=100,
            t=5,
            pad=1
        ),
    )
    trace = go.Pie(labels=labels, values=values, marker=dict(
        colors=colors), direction="counter-clockwise")
    fig = go.Figure(data=[trace], layout=layout)
    return py.plot(fig, output_type='div', show_link=False)

def mapGraph(year):
    usages = Usage.objects.filter(dateTime__year=year).values('ip').exclude(ip='') \
        .annotate(usage_count=Count('ip')) #get ip's and counts
    jsonData=[]

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
                'Lon':float(loc.longitude),
                'Lat':float(loc.latitude),
                'Country':str(loc.country),
                'ip':str(loc.ip),
                'Year':year,
                'Value':count,
            }
        )
    if len(jsonData) == 0:
        return "<div>No Location data for this year.</div>"
    usage_locations = pandas.DataFrame(jsonData)
    cases = []
    for _, row in usage_locations.iterrows():
        cases.append(
            go.Scattergeo(
                lon=[row['Lon']],
                lat=[row['Lat']],
                text='%d %s' % (row['Value'],row['Country']),
                name=row['Country'],
                marker=dict(
                    size=10, #row['Value']/20.0,
                    color='#FF3333',
                    line=dict(width=0)
                ),
                mode = 'markers+text',
                textposition = 'bottom center'
            )
        )
    layout = go.Layout(
        title='Location Data',
        width=1100,
        height=600,
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
        legend=dict(traceorder='reversed')
        # Put newer and larger circles at the z-bottom so the old ones show up
    )
    fig = go.Figure(layout=layout, data=cases)
    div = py.plot(fig, validate=False, output_type='div', show_link=False)
    return div
