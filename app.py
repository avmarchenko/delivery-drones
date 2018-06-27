# -*- coding: utf-8 -*-
# Copyright 2018 Alex Marchenko
# Distributed under the terms of the Apache License 2.0
"""
Delivery Drone Monitor
################################
A simple frontend demo that monitors the recently seen
drone proximity. Ass
"""
import dash
import uuid
import random
import dash_core_components as dcc
import dash_html_components as html
import dronedirector as dd
from datetime import datetime
from happybase import Connection


# Example drones
rd = random.Random()
rd.seed(0)
uid0 = uuid.UUID(int=rd.getrandbits(128))
rd.seed(1)
uid1 = uuid.UUID(int=rd.getrandbits(128))
rd.seed(2)
uid2 = uuid.UUID(int=rd.getrandbits(128))
d0 = dd.SinusoidalDrone(1000.0, 41.0, "New York County", uid=uid0, speed=0.01)
d1 = dd.SinusoidalDrone(1000.0, 41.0, "New York County", uid=uid1, speed=0.02)
d2 = dd.SinusoidalDrone(1000.0, 41.0, "New York County", uid=uid2, speed=0.03)


app = dash.Dash("Drone Director")
header = [html.H1(children="Drone Director"),
          html.H2(children="Monitoring the relative proximity of simulated delivery drones!")]
app.layout = html.Div(children=header)


def describe_proximity(interval, window_ms=6000):
    """
    Poll the DB at a given interval to get the minimum proximity and average proximity

    Args:
        interval (int): Inteval at which to update
        window_ms (int): Window range for averaging (in milliseconds)
    """
    datetime.datetime.now() - datetime.timedelta(milliseconds=window_ms)

    pass




if __name__ == '__main__':
    app.run_server(debug=True, port=80, host="0.0.0.0")
