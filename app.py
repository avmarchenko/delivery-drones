# -*- coding: utf-8 -*-
# Copyright 2018 Alex Marchenko
# Distributed under the terms of the Apache License 2.0
"""
Delivery Drone Monitor
################################
A simple frontend demo that monitors the recently seen
drone proximity.

Note:
    The app assumes that the database it is connecting to
    is running locally: change as necessary.
"""
from __future__ import print_function, division
import dash
import uuid
import json
import random
import numpy as np
import pandas as pd
from collections import deque
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.graph_objs import Figure, Scatter
import dronedirector as dd
from happybase import Connection
from dronedirector.aerial import dtfmt    # Import this stuff to the base namespace
from datetime import datetime             # for speed.
from datetime import timedelta


# Configuration matches that as used for dronestorm
with open("/opt/internal.json") as f:
    config = json.load(f)
# Example drones
ndrones = 10
rd = random.Random()
drones = []
for i in range(ndrones):
    rd.seed(i)
    uid = uuid.UUID(int=rd.getrandbits(128))
    drones.append(dd.SinusoidalDrone(1000.0, 41.0, "New York County", uid=uid, speed=(i+1*10)))
pks = []
for i in range(ndrones):
    for j in range(i+1, ndrones):
        pks.append(drones[i].uid.hex + drones[j].uid.hex)


app = dash.Dash("Drone Director")
header = [html.H1(children="Drone Director"),
          html.H2(children="Monitoring the relative proximity of simulated delivery drones!")]
graph = dcc.Graph(id='describe_proximity')
graphdiv = html.Div([graph], style=dict(margin='auto', width="80%", height="auto", display="inline-block"))
graphint = dcc.Interval(id="meanup", interval=3000, n_intervals=0)
app.layout = html.Div(children=header+[graphdiv, graphint])
maxlen =1000
time = deque(maxlen=maxlen)
avgy = deque(maxlen=maxlen)
miny = deque(maxlen=maxlen)


@app.callback(Output('describe_proximity', 'figure'), [Input('meanup', 'n_intervals')])
def describe_proximity(window_seconds=5):
    """
    Poll the DB at a given interval to get the minimum proximity, average proximity
    and the variance in the mean (to get a feel for range sampled).

    Args:
        interval (int): Inteval at which to update
        window_ms (int): Window range for averaging (in milliseconds)
    """
    dt = timedelta(seconds=window_seconds)
    now_ = datetime.now()
    start = (now_ - dt).strftime(dtfmt)
    stop = now_.strftime(dtfmt)
    conn = Connection(config['hbase'], port=int(config['thrift']))
    tab = conn.table(str.encode(config['prox_table']))
    #dct = {k: v for k, v in tab.scan(row_start=pk01+start, row_stop=pk01+stop)}
    avg_ = []
    min_ = 0
    for pk in pks:
        dct = {k: v for k, v in tab.scan(row_start=pk+start, row_stop=pk+stop)}
        if len(dct) > 0:
            df = pd.DataFrame.from_dict(dct, orient="index").reset_index()
            df[b'spatial:dr'] = df[b'spatial:dr'].astype(float)
            avg_.append(df[b'spatial:dr'].mean())
            min_ += df[df[b'spatial:dr'] < 10].shape[0]

    time.append(str(now_))
    miny.append(min_)
    try:
        avgy.append(sum(avg_)/len(avg_))
    except Exception:
        avgy.append(np.nan)
    avgline = Scatter(x=list(time), y=list(avgy), type='scatter', mode='lines', name='Mean')
    minline = Scatter(x=list(time), y=list(miny), type='scatter', mode='lines', name='< 10', yaxis="y2")
    #trace = [{'x': time, 'y': avgy, 'type': "scatter", 'mode': "lines", 'name': 'Avg'},
    #         {'x': time, 'y': miny, 'type': "scatter", 'mode': "lines", 'name': 'Min'}]
    layout = {'height': 620, 'yaxis': {'title': "Average Proximity (m)", 'side': "left"},
              'yaxis2': {'title': 'Within 10 Meters (count)', 'side': "right", 'overlaying': "y"}}
    return Figure(data=[avgline, minline], layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True, port=80, host="0.0.0.0")
