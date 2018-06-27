# -*- coding: utf-8 -*-
# Copyright 2018 Alex Marchenko
# Distributed under the terms of the Apache License 2.0
"""
Delivery Drone Monitor
################################
"""
import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash()
app.layout = html.Div(children=[html.H1(children="Delivery Drones"),
                                html.Div(children="""Monitoring the proximity of simulated delivery drones to one another."""),
                                dcc.Graph(id="example-graph",
                                          figure={'data': [
                                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                        ], 'layout': {'title': 'Example'}})])

if __name__ == '__main__':
    app.run_server(debug=True, port=80, host="0.0.0.0")
