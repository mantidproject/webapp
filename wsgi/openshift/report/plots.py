#!/usr/bin/env python

import plotly
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

OS_LIST = ["Windows", "Mac", "RHEL", "Ubuntu", "Other"]
# RHEL or Red Hat or RedHat? Which is better for the project?

years = ["2016", "2017"]
year_2016_data = {"Windows": 30, "Mac": 40,
                  "RHEL": 70, "Ubuntu": 62, "Other": 10}
year_2017_data = {"Windows": 32, "Mac": 45,
                  "RHEL": 80, "Ubuntu": 72, "Other": 20}
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
    Windows = [year_2016_data["Windows"], year_2017_data["Windows"]]
    Mac = [year_2016_data["Mac"], year_2017_data["Mac"]]
    RHEL = [year_2016_data["RHEL"], year_2017_data["RHEL"]]
    Ubuntu = [year_2016_data["Ubuntu"], year_2017_data["Ubuntu"]]
    Other = [year_2016_data["Other"], year_2017_data["Other"]]
    # There must be a more compact way to do this.

    Total = [0, 0]
    for OS_count in OS_LIST:
        Total[0] += year_2016_data[OS_count]
        Total[1] += year_2017_data[OS_count]
    # The array has one value per year. Total[0] is 2016, Total[1] is 2017.

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
        barmode='group',
        width=700,
        height=700,
        margin=go.Margin(
            l=50,
            r=0,
            b=100,
            t=100,
            pad=1
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    div = py.plot(fig, output_type='div', show_link=False)
    return div


def pieChart():
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
            t=10,
            pad=1
        ),
    )
    trace = go.Pie(labels=labels, values=values, marker=dict(
        colors=colors), direction="counter-clockwise")
    fig = go.Figure(data=[trace], layout=layout)
    return py.plot(fig, output_type='div')


def mapGraph():
    ds = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/2014_ebola.csv')
    """
    Country,Month,Year,Lat,Lon,Value
    Guinea, 3, 14, 9.95, -9.7, 122
    Guinea,4,14,9.95,-9.7,224
    Guinea,5,14,9.95,-9.7,291
    Guinea,6,14,9.95,-9.7,413
    Guinea,7,14,9.95,-9.7,460
    Guinea,8,14,9.95,-9.7,771
    Guinea,9,14,9.95,-9.7,1022
    Guinea,10,14,9.95,-9.7,
    Guinea,11,14,9.95,-9.7,
    Guinea,12,14,9.95,-9.7,
    Liberia,4,14,6.43,-9.43,35
    Liberia,5,14,6.43,-9.43,13
    Liberia,6,14,6.43,-9.43,107
    Liberia,7,14,6.43,-9.43,329
    Liberia,8,14,6.43,-9.43,1395
    Liberia,9,14,6.43,-9.43,3362
    Liberia,10,14,6.43,-9.43,
    Liberia,11,14,6.43,-9.43,
    Liberia,12,14,6.43,-9.43,
    Mali,10,14,17.57,-4,1
    Mali,11,14,17.57,-4,8
    Senegal,8,14,14.5,-14.45,1
    Senegal,9,14,14.5,-14.45,3
    Sierra Leone,5,14,8.46,-11.78,50
    Sierra Leone,6,14,8.46,-11.78,239
    Sierra Leone,7,14,8.46,-11.78,533
    Sierra Leone,8,14,8.46,-11.78,1216
    Sierra Leone,9,14,8.46,-11.78,1940
    Sierra Leone,10,14,8.46,-11.78,
    Sierra Leone,11,14,8.46,-11.78,
    Sierra Leone,12,14,8.46,-11.78,
    """
    df = ds.append([
        {
            'Country': "United States",
            'Month': 7,
            'Year': 14,
            'Lat': 35.0,
            'Lon': -87.0,
            'Value': 500
        },
        {
            'Country': "United States",
            'Month': 9,
            'Year': 14,
            'Lat': 35.0,
            'Lon': -87.0,
            'Value': 2000
        },
        {
            'Country': "Great Britain",
            'Month': 7,
            'Year': 14,
            'Lat': 52.0,
            'Lon': -1.0,
            'Value': 500
        },
        {
            'Country': "Great Britain",
            'Month': 9,
            'Year': 14,
            'Lat': 52.0,
            'Lon': -1.0,
            'Value': 1000
        },
        {
            'Country': "France",
            'Month': 7,
            'Year': 14,
            'Lat': 47.0,
            'Lon': 3.0,
            'Value': 125
        },
        {
            'Country': "France",
            'Month': 9,
            'Year': 14,
            'Lat': 47.0,
            'Lon': 3.0,
            'Value': 730
        },
        {
            'Country': "Australia",
            'Month': 7,
            'Year': 14,
            'Lat': -25.0,
            'Lon': 140.0,
            'Value': 300
        },
        {
            'Country': "Australia",
            'Month': 9,
            'Year': 14,
            'Lat': -25.0,
            'Lon': 140.0,
            'Value': 891
        },
    ], ignore_index=True)

    # df.head() returns first five
    colors = ['#DDBBBB', '#EE0000', '#CC2222', '#FF3333']
    months = {6: 'June', 7: 'July', 8: 'Aug', 9: 'Sept'}
    cases = []
    for i in range(6, 10)[::-1]:
        cases.append(
            go.Scattergeo(
                lon=df[df['Month'] == i]['Lon'],  # -(max(range(6,10))-i),
                lat=df[df['Month'] == i]['Lat'],
                text=df[df['Month'] == i]['Value'],
                name=months[i],
                marker=dict(
                    size=df[df['Month'] == i]['Value'] / 50,
                    color=colors[i - 6],
                    line=dict(width=0)
                )
            )
        )
    cases[0]['text'] = df[df['Month'] == 9]['Value'].map('{:.0f}'.format) \
        .astype(str) + ' ' + df[df['Month'] == 9]['Country']
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
            scope='world',
            showframe=True,
            showcoastlines=True,
            showland=True,
            landcolor="rgb(229, 229, 229)",
            countrycolor="rgb(255, 255, 255)",
            coastlinecolor="rgb(255, 255, 255)",
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
            l=0,
            r=50,
            b=100,
            t=30,
            pad=1
        ),
        legend=dict(traceorder='reversed')
        # Put newer and larger circles at the z-bottom so the old ones show up
    )
    fig = go.Figure(layout=layout, data=cases)
    div = py.plot(fig, validate=False, output_type='div')
    return div
