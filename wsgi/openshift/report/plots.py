#!/usr/bin/env python

import plotly
import plotly.offline as py
import plotly.graph_objs as go

def aFunc():
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
       name="Total"
    )

    WindowsTrace = go.Bar(
        x=years,
        y=Windows,
        name="Windows"
    )
    MacTrace = go.Bar(
        x=years,
        y=Mac,
        name="Mac"
    )

    RedHatTrace = go.Bar(
        x=years,
        y=RedHat,
        name="Red Hat"
    )

    UbuntuTrace = go.Bar(
        x=years,
        y=Ubuntu,
        name="Ubuntu"
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