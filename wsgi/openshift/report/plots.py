#!/usr/bin/env python

import plotly
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

def graph1():
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
    Windows=[20, 14, 23]
    Mac=[12, 18, 29]
    RedHat=[18, 35, 12]
    Ubuntu=[16, 30, 15]
    Total=[]

    for i in range(len(Windows)):
        Total.append(Windows[i] + Mac[i] + RedHat[i] + Ubuntu[i])

    TotalTrace = go.Bar(
        x=years,
        y=Total,
        name="Total",
        marker=dict(
            color='rgb(150,220,150)',
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
        width=1000,
        height=700,
        margin=go.Margin(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    div = py.plot(fig, output_type='div', show_link=False)
    return div


def map():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_ebola.csv')
    df.head()
    cases = []
    colors = ['rgb(239,243,255)','rgb(189,215,231)','rgb(107,174,214)','rgb(33,113,181)']
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
    inset = [
        go.Choropleth(
            locationmode = 'country names',
            locations = df[ df['Month'] == 9 ]['Country'],
            z = df[ df['Month'] == 9 ]['Value'],
            text = df[ df['Month'] == 9 ]['Country'],
            colorscale = [[0,'rgb(0, 0, 0)'],[1,'rgb(0, 0, 0)']],
            autocolorscale = False,
            showscale = False,
            geo = 'geo2'
        ),
        go.Scattergeo(
            lon = [21.0936],
            lat = [7.1881],
            text = ['Africa'],
            mode = 'text',
            showlegend = False,
            geo = 'geo2'
        )
    ]
    #
    # LAYOUT SETTINGS HERE
    #
    layout = go.Layout(
        title = 'Data showing increased instance over time<br>',
    #Source: <a href="https://data.hdx.rwlabs.org/dataset/rowca-ebola-cases">\
    #HDX</a>',
        width=1000,
        height=700,
        geo = dict(
            resolution = 50,
            scope = 'africa',
            showframe = False,
            showcoastlines = True,
            showland = True,
            landcolor = "rgb(229, 229, 229)",
            countrycolor = "rgb(255, 255, 255)" ,
            coastlinecolor = "rgb(255, 255, 255)",
            projection = dict(
                type = 'Mercator'
            ),
            lonaxis = dict( range= [ -15.0, -5.0 ] ),
            lataxis = dict( range= [ 0.0, 12.0 ] ),
            domain = dict(
                x = [ 0, 1 ],
                y = [ 0, 1 ]
            )
        ),
        geo2 = dict(
            scope = 'africa',
            showframe = False,
            showland = True,
            landcolor = "rgb(229, 229, 229)",
            showcountries = False,
            domain = dict(
                x = [ 0, 0.6 ],
                y = [ 0, 0.6 ]
            ),
            bgcolor = 'rgba(255, 255, 255, 0.0)',
        ),
        legend = dict(
            traceorder = 'reversed'
        )
    )
    fig = go.Figure(layout=layout, data=cases+inset)
    div = py.plot( fig, validate=False, output_type='div')
    return div