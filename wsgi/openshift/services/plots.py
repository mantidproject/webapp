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

OS_LIST = ["Windows", "Mac", "RHEL", "Ubuntu", "Other"]
# RHEL or Red Hat or RedHat? Which is better for the project?
start = datetime.date(2006,1,1)
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
        name="Mac",
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
        name="Other",
        marker=dict(
            color=OTHER_COLOR,
        ),
    )

    data = [TotalTrace, WindowsTrace, MacTrace,
            RedHatTrace, UbuntuTrace, OtherTrace]
    layout = go.Layout(
        xaxis=dict(
            range=[now.year-2, now.year+0.5] # custom x-axis scaling
        ),
        barmode='group',
        width=650,
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
    usages = Usage.objects.filter(dateTime__year=year).values('osName').exclude(ip='') \
        .annotate(usage_count=Count('osName')) #get OS's and counts
    if not usages:
        return "Error: No OS data for this year."
    for obj in usages.iterator():
        if obj["osName"] == "Windows NT":
            labels.append("Windows")
            colors.append(WIN_COLOR)
        elif obj["osName"] == "Darwin":
            labels.append("Mac")
            colors.append(MAC_COLOR)
        elif obj["osName"] == "Linux":
            labels.append("Linux")
            colors.append(RHEL_COLOR)
        else:
            labels.append("Other (%s)" % obj["osName"])
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
    start = time.time()
    print '***** 00'
    usages = Usage.objects.filter(dateTime__year=year).values('ip').exclude(ip='') \
        .annotate(usage_count=Count('ip')) #get ip's and counts
    jsonData=[]

    print '***** 11[', time.time() - start ,'] '
    for obj in usages.iterator():
        if len(obj['ip']) == 0:
            continue
        print 'Entry:', obj['ip'], time.time() - start
        count = obj['usage_count']
        try:
            loc = Location.objects.get(ip=obj['ip'])
            print "Match"#,loc.ip
        except ObjectDoesNotExist:
            # No match for given IP
            print "No Match" #, obj['ip']
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
    print '***** 20[', time.time() - start ,'] '
    if len(jsonData) == 0:
        return "<div>No Location data for this year.</div>"
    print '***** 22[', time.time() - start ,'] '
    usage_locations = pandas.DataFrame(jsonData)
    print usage_locations
    cases = []
    #print '*****', jsonData
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
    print '***** 30[', time.time() - start ,'] '
    layout = go.Layout(
        title='Appropriate Title Here',
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
