import uuid
import random
import numpy as np
import happybase as hb
from itertools import cycle
from streamparse import Spout
from datetime import datetime


dtfmt = "%Y%m%d%H%M%S%f"


class TestCoordinateSpout(Spout):
    outputs = ['id0', 'id1', 'alt0', 'alt1', 'lat0', 'lat1', 'lon0', 'lon1', 't0', 't1']

    def initialize(self, stormconf, context):
        self.lon = cycle(np.sin(np.arange(0, 10*np.pi, np.pi/(360*50))))
        self.lon_ = cycle(np.sin(np.arange(0, 20*np.pi, np.pi/(360*25))))
        self.lat = cycle([0.7])    #cycle(np.arange(0.69, 0.72, 0.001))
        self.alt = cycle([1000.0])    #cycle([900.0, 950.0, 1000.0, 1100.0])
        rd = random.Random()
        rd.seed(0)
        self.id0 = uuid.UUID(int=rd.getrandbits(128))
        rd.seed(1)
        self.id1 = uuid.UUID(int=rd.getrandbits(128))
        self.conn = hb.Connection("10.0.0.13", port=16050)
        self.raw = self.conn.table(b"drones_raw")

    def next_tuple(self):
        t0 = datetime.now()
        id0 = self.id0.hex
        id1 = self.id1.hex
        alt0 = next(self.alt)
        alt1 = next(self.alt)
        lat0 = next(self.lat)
        lat1 = next(self.lat)
        lon0 = next(self.lon)
        lon1 = next(self.lon_)
        t1 = datetime.now()
        rowkey0 = str.encode(id0 + t0.strftime(dtfmt))
        self.raw.put(rowkey0, {b'uuid:uuid': str.encode(id0),
                               b'datetime:datetime': str.encode(str(t0)),
                               b'spatial:alt': str.encode(str(alt0)), 
                               b'spatial:lat': str.encode(str(lat0)),
                               b'spatial:lon': str.encode(str(lon0))})
        rowkey1 = str.encode(id1 + t1.strftime(dtfmt))
        self.raw.put(rowkey1, {b'uuid:uuid': str.encode(id1),
                               b'datetime:datetime': str.encode(str(t1)),
                               b'spatial:alt': str.encode(str(alt1)), 
                               b'spatial:lat': str.encode(str(lat1)),
                               b'spatial:lon': str.encode(str(lon1))})
        self.emit([id0, id1, alt0, alt1, lat0, lat1, lon0, lon1, t0.strftime(dtfmt), t1.strftime(dtfmt)])
