from models import Location, Usage
from django.db.models import Count
import plotly
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd
import datetime

OS_LIST = ["Windows", "Mac", "RHEL", "Ubuntu", "Other"]
# RHEL or Red Hat or RedHat? Which is better for the project?
now = datetime.datetime.today()
start = datetime.date(2006,1,1)
years_generated = range(start.year, now.year+1)
print years_generated

years = years_generated #["2016", "2017"]
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

year_2016_data = {"Windows": 30, "Mac": 40, 
                  "RHEL": 70, "Ubuntu": 62, "Other": 10
}
year_2017_data = {"Windows": 92, "Mac": 45,
                  "RHEL": 80, "Ubuntu": 72, "Other": 20
}

# Let's just work with this as a given.
# It's eventually going to need geolocation functionality though, so long term..


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
    """    
    Windows = [year_2016_data["Windows"], year_2017_data["Windows"]]
    Mac = [year_2016_data["Mac"], year_2017_data["Mac"]]
    RHEL = [year_2016_data["RHEL"], year_2017_data["RHEL"]]
    Ubuntu = [year_2016_data["Ubuntu"], year_2017_data["Ubuntu"]]
    Other = [year_2016_data["Other"], year_2017_data["Other"]]

    Total = [0, 0]
    for OS_count in OS_LIST:
        Total[0] += year_2016_data[OS_count]
        Total[1] += year_2017_data[OS_count]
    # The array has one value per year. Total[0] is 2016, Total[1] is 2017.
    """
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
    links = "<div id='links'>"
    for year in years:
        links += "<a href = '/plots/year/"+str(year)+"'> "+str(year)+"</a><br />"
    links += "</div>"
    print links
    return div + links


def pieChart(year):
    # sinful. clean it.
    # labels = ['Windows', 'Mac', 'Red Hat', 'Ubuntu', 'Other']
    labels = []
    values = []
    for os in OS_LIST:
        labels.append(os)
        values.append(all_time_data[year][os])
        """
    values = [
        year_2017_data['Windows'], year_2017_data['Mac'],
        year_2017_data['RHEL'], year_2017_data['Ubuntu'],
        year_2017_data['Other']
    ]
    """
    colors = [WIN_COLOR, MAC_COLOR, RHEL_COLOR, UBUNTU_COLOR, OTHER_COLOR]
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
    #dateTime="2014-12-11T19:46:40"
    usages = Usage.objects.filter(dateTime__year=year)\
        .values('ip').annotate(usage_count=Count('ip'))
    #print "Usages in "+year+":", usages
    locs_matching = Location.objects.filter(ip__in = usages.values_list('ip', flat=True)) 
    locs_count = locs_matching.count()
    # only get locations whose IP addresses correlate to usages for this year

    # SELECT longitude, latitude, country from `location` WHERE ip IN
    # (SELECT ip from `usage` WHERE year = (current_year))

    """ Next Step:
        - group usages by common ip (and only for selected year)
        - assign counts to each usage
        - get location data for each usage
        - display
        
    """
    print usages
    print 
    print locs_matching
    #print locs_count,"matching Locations:", locs_matching
    locs = locs_matching#Location.objects.all()
    if locs_count == 0:
        return "<div>No Location data for this year.</div>"
    jsonData=[]
    for obj in locs:
        jsonData.append(
            {
            'Lon':float(obj.longitude),
            'Lat':float(obj.latitude),
            'Country':str(obj.country),
            'ip':str(obj.ip),
            'Year':year,
            'Value':int(500),
            }
        )
    for obj in jsonData:
        usage = usages.filter(ip=obj["ip"])
        count = usage.values_list('usage_count', flat=True)
        print count[0]
        obj["Value"] = count[0]
    webster = pd.DataFrame(jsonData)
    print webster
    # df.head() returns first five
    colors = ['#DDBBBB', '#EE0000', '#CC2222', '#FF3333']
    cases = []
    for i in locs.values_list('ip', flat=True): #range(6, 10)[::-1]:
        cases.append(
            go.Scattergeo(
                lon=webster[webster['ip'] == i]['Lon'],  # -(max(range(6,10))-i),
                lat=webster[webster['ip'] == i]['Lat'],
                text=webster[webster['ip'] == i]['Value'].map('{:.0f}'.format) \
                .astype(str) + ' ' + webster[webster['ip'] == i]['Country'],
                name=webster[webster['ip'] == i]['ip'],
                marker=dict(
                    size=webster[webster['ip'] == i]['Value'] / 20,
                    color=colors[3],
                    line=dict(width=0)
                ),
                mode = 'markers+text',
                textposition = 'bottom center'
            )
        )


    layout = go.Layout(
        title='Appropriate Title Here',
        # <a href="https://data.hdx.rwlabs.org/dataset/rowca-ebola-cases">\
        # Source: HDX</a>',
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
