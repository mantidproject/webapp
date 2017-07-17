#!/usr/bin/env python

import plotly
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

year_2017_data = {"Windows": 32, "Mac": 45, "RHEL": 80, "Ubuntu": 72, "Other": 20}
# Let's just work with this as a given. 

def main():
    years=["2015", "2016", "2017"]
    """
    DataSet = {
        'Windows':  [20, 14, 23], 
        'Mac':      [12, 18, 29], 
        'Linux':    [18, 35, 12], 
        'Total':    []
    } 
    """
    datasetNames=['Windows', 'Mac', 'RedHat', 'Ubuntu', 'Total']
    Windows=    [20, 14, 23]
    Mac=        [12, 18, 29]
    RedHat=     [18, 35, 12]
    Ubuntu=     [16, 30, 15]
    Total=[]

    for i in range(len(Windows)):
        Total.append(Windows[i] + Mac[i] + RedHat[i] + Ubuntu[i])

    TotalTrace = go.Bar(
        x=years,
        y=Total,
        name="Total",
        marker=dict(
            color='rgb(200,200,200)',
            #color='rgb(150,50,250)',
        ),
    )

    WindowsTrace = go.Bar(
        x=years,
        y=Windows,
        name="Windows",
        marker=dict(
            color='rgb(70,70,220)',
        ),
    )
    MacTrace = go.Bar(
        x=years,
        y=Mac,
        name="Mac",
        marker=dict(
            color='rgb(190,200,250)',
        ),
    )

    RedHatTrace = go.Bar(
        x=years,
        y=RedHat,
        name="Red Hat",
        marker=dict(
            color='rgb(200,80,80)',
        ),
    )

    UbuntuTrace = go.Bar(
        x=years,
        y=Ubuntu,
        name="Ubuntu",
        marker=dict(
            color='rgb(250,160,100)',
        ),
    )
    data = [TotalTrace, WindowsTrace, MacTrace, RedHatTrace, UbuntuTrace]
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


def map():
    ds = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_ebola.csv')
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
        'Country':"United States",
        'Month':7,
        'Year':14,
        'Lat':35.0,
        'Lon':-87.0,
        'Value':500
        },
        {
        'Country':"United States",
        'Month':9,
        'Year':14,
        'Lat':35.0,
        'Lon':-87.0,
        'Value':2000
        },
        {
        'Country':"Great Britain",
        'Month':7,
        'Year':14,
        'Lat':52.0,
        'Lon':-1.0,
        'Value':500
        },
        {
        'Country':"Great Britain",
        'Month':9,
        'Year':14,
        'Lat':52.0,
        'Lon':-1.0,
        'Value':1000
        },
        {
        'Country':"France",
        'Month':7,
        'Year':14,
        'Lat':47.0,
        'Lon':3.0,
        'Value':125
        },
        {
        'Country':"France",
        'Month':9,
        'Year':14,
        'Lat':47.0,
        'Lon':3.0,
        'Value':730
        },
        {
        'Country':"Australia",
        'Month':7,
        'Year':14,
        'Lat':-25.0,
        'Lon':140.0,
        'Value':300
        },
        {
        'Country':"Australia",
        'Month':9,
        'Year':14,
        'Lat':-25.0,
        'Lon':140.0,
        'Value':891
        },
     ], ignore_index=True)
    df.head()
    cases = []
    colors = ['#DDBBBB', '#EE0000', '#CC2222', '#FF3333']#['rgb(239,243,255)','rgb(189,215,231)','rgb(107,174,214)','rgb(33,113,181)']
    months = {6:'June',7:'July',8:'Aug',9:'Sept'}
    for i in range(6,10)[::-1]:
        cases.append(go.Scattergeo(
                lon = df[ df['Month'] == i ]['Lon'], #-(max(range(6,10))-i),
                lat = df[ df['Month'] == i ]['Lat'],
                text = df[ df['Month'] == i ]['Value'],
                name = months[i],
                marker = dict(
                    size = df[ df['Month'] == i ]['Value']/50,
                    color = colors[i-6],
                    line = dict(width = 0)
                )
            )
        )
    cases[0]['text'] = df[ df['Month'] == 9 ]['Value'].map('{:.0f}'.format).astype(str)+' '+\
        df[ df['Month'] == 9 ]['Country']
    cases[0]['mode'] = 'markers+text'
    cases[0]['textposition'] = 'bottom center'
    #
    # LAYOUT SETTINGS HERE
    #
    layout = go.Layout(
        title = 'Data showing increased instance over time<br>',
    #Source: <a href="https://data.hdx.rwlabs.org/dataset/rowca-ebola-cases">\
    #HDX</a>',
        width=1100,
        height=600,
        geo = dict(
            resolution = 5,
            scope = 'world',
            showframe = False,
            showcoastlines = True,
            showland = True,
            landcolor = "rgb(229, 229, 229)",
            countrycolor = "rgb(255, 255, 255)" ,
            coastlinecolor = "rgb(255, 255, 255)",
            projection = dict(
                type = 'Mercator'
            ),
            lonaxis = dict( range= [ -150.0, 150.0 ] ),
            lataxis = dict( range= [ -100.0, 100.0 ] ),
            domain = dict(
                x = [ 0, 1 ],
                y = [ 0, 1 ]
            )
        ),
        margin=go.Margin(
            l=0,
            r=50,
            b=100,
            t=30,
            pad=1
        ),
        legend = dict(
            traceorder = 'reversed'
        )
    )
    fig = go.Figure(layout=layout, data=cases) #cases+inset
    div = py.plot( fig, validate=False, output_type='div')
    return div

def pi():
    labels=['Windows','Mac','Red Hat','Ubuntu', 'Other']
    values=[
            year_2017_data['Windows'], year_2017_data['Mac'],
            year_2017_data['RHEL'], year_2017_data['Ubuntu'],
            year_2017_data['Other']
            ]
    colors = ['rgb(70,70,220)', 'rgb(190,200,250)', 'rgb(200,80,80)', 'rgb(250,160,100)', 'rgb(110,112,100)']
    layout = go.Layout(
        width = 500,
        height = 500,
        margin=go.Margin(
            l=0,
            r=50,
            b=100,
            t=10,
            pad=1
        ),
    )
    trace = go.Pie(labels=labels, values=values, marker=dict(colors=colors))
    fig = go.Figure(data=[trace], layout=layout)
    return py.plot(fig, output_type='div')