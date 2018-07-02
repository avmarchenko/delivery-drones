# Real Time Monitoring of Delivery Drones
This project utilizes a drone simulation package and an Apache Storm
topology to create a pipeline that processes drone location (altitude,
latitude, and longitude) streams and processes relative distances between
them. The subpackage [dronedirector](https://github.com/avmarchenko/dronedirector)
is used to create drone objects. The subpackage [dronestorm](https://github.com/avmarchenko/dronestorm)
is an example topology defined using [streamparse](https://github.com/Parsely/streamparse).
The files provided here can be used to stand up a simple monitoring application using
[Dash](https://github.com/plotly/dash).


# Cloud Configuration
An example cloud configuration is as follows.

    1. 1 Kafka server
    2. 4 Hadoop servers (Hadoop/YARN/HBase)
    3. 1 Web server

# Monitoring
After configuring a cluster, in one terminal (for example),

    $ python fly_some_drones.py

and in another terminal.

    $ python app.py
