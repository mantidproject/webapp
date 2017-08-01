from models import Location
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
all_time = {
    "2006": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2007": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2008": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2009": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2010": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2011": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2012": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2013": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2014": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2015": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
    },
    "2016": {
        "Windows": 30, "Mac": 40, "RHEL": 70, "Ubuntu": 62, "Other": 10
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
    for year in all_time:
        year_total = 0
        Windows.append(all_time[year]["Windows"])
        Mac.append(all_time[year]["Mac"])
        RHEL.append(all_time[year]["RHEL"])
        Ubuntu.append(all_time[year]["Ubuntu"])
        Other.append(all_time[year]["Other"])
        Total.append(sum(all_time[year].values()))
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
    return div


def pieChart(year):
    # sinful. clean it.
    labels = ['Windows', 'Mac', 'Red Hat', 'Ubuntu', 'Other']
    values = [
        year_2017_data['Windows'], year_2017_data['Mac'],
        year_2017_data['RHEL'], year_2017_data['Ubuntu'],
        year_2017_data['Other']
    ]
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

    locs = Location.objects.all()
    jsonData=[]
    for obj in locs:
        jsonData.append(
            {
            'Lon':float(obj.longitude),
            'Lat':float(obj.latitude),
            'Country':str(obj.country),
            #'ip':str(obj.ip),
            'Month':int(9),
            'Year':int(14),
            'Value':int(500),
            }
        )
    webster = pd.DataFrame(jsonData)
    print webster
    # df.head() returns first five
    colors = ['#DDBBBB', '#EE0000', '#CC2222', '#FF3333']
    months = {6: 'June', 7: 'July', 8: 'Aug', 9: 'Sept'}
    cases = []
    for i in range(6, 10)[::-1]:
        cases.append(
            go.Scattergeo(
                lon=webster[webster['Month'] == i]['Lon'],  # -(max(range(6,10))-i),
                lat=webster[webster['Month'] == i]['Lat'],
                text=webster[webster['Month'] == i]['Value'],
                name=months[i],
                marker=dict(
                    size=webster[webster['Month'] == i]['Value'] / 50,
                    color=colors[i - 6],
                    line=dict(width=0)
                )
            )
        )
        cases[0]['text'] = webster[webster['Month'] == 9]['Value'].map('{:.0f}'.format) \
        .astype(str) + ' ' + webster[webster['Month'] == 9]['Country']
    # Set label as most recent value (sept) and the country's name
        cases[0]['mode'] = 'markers+text'
        cases[0]['textposition'] = 'bottom center'

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
