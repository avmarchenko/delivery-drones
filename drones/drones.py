# -*- coding: utf-8 -*-
# Copyright 2018 Alex Marchenko
# Distributed under the terms of the Apache License 2.0
"""
Drones
##########
This module provides some simple classes that are used to simulate flying
drones.
"""
from abc import ABC, abstractmethod


class AbstractAerialObject:
    """
    Abstract base class for aerial objects.


    This class
    """
    def __init__(self, altitude, latitude, longitude):
        pass


class SinusoidalDrone(Drone):
    """
    """
