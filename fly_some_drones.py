# -*- coding: utf-8 -*-
# Copyright 2018 Alex Marchenko
# Distributed under the terms of the Apache License 2.0
"""
Simple Drone Flyer
################################
"""
from __future__ import division, print_function, absolute_import
import dronedirector as dd
from dronedirector.producer import fly_drones
import uuid, random


rd = random.Random()
ndrones = 10
drones = []
for i in range(ndrones):
    rd.seed(i)
    uid = uuid.UUID(int=rd.getrandbits(128))
    drones.append(dd.SinusoidalDrone(1000.0, 41.0, "New York County", uid=uid, speed=(i+1*10)))

fly_drones("10.0.0.13", 72000, drones=drones, time_delay=1.5)
