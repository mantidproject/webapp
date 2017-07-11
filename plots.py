#!/usr/bin/env python

import plotly
import plotly.offline as py
import plotly.graph_objs as go

years=["2015", "2016", "2017"]
DataSet = {
    'Windows':  [20, 14, 23], 
    'Mac':      [12, 18, 29], 
    'Linux':    [18, 35, 12], 
    'Total':    []
} 
"""
datasetNames=['Windows', 'Mac', 'Linux', 'Total']
Windows=[20, 14, 23]
Mac=[12, 18, 29]
Linux=[18, 35, 12]
Total=[]
"""
for i in range(len(DataSet['Windows'])):
    DataSet['Total'].append( DataSet['Windows'][i] + DataSet['Mac'][i] + DataSet['Linux'][i])

print DataSet['Total']

WindowsTrace = go.Bar(
    x=years,
    y=DataSet['Windows'],
    name="Windows"
)
MacTrace = go.Bar(
    x=years,
    y=DataSet['Mac'],
    name="Mac"
)

LinuxTrace = go.Bar(
    x=years,
    y=DataSet['Linux'],
    name="Linux"
)

TotalTrace = go.Bar(
    x=years,
    y=DataSet['Total'],
    name="Total"
)

data = [WindowsTrace, MacTrace, LinuxTrace, TotalTrace]
layout = go.Layout(barmode='group')
fig = go.Figure(data=data, layout=layout)

py.plot(fig, filename='pi-chart.html')
