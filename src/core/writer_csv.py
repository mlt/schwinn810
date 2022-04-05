""" Simple CSV writer for Schwinn 810 """

import sys,os
import subprocess
import csv
import logging
from writer import *

_log = logging.getLogger(__name__)

open_extra = {}
if sys.version_info >= (3,0):
    open_extra["newline"] = ''

class WriterCSV(Writer):
    """ Default files writer """

    track_keys = ["Start", "End", "Laps", "MaxHeart", "Heart", "MaxSpeed", \
                      "Speed", "x4", "x5", "Points", "Track"]
    lap_keys = ["Time", "Speed", "Lap", "Distance", "kcal", "MaxSpeed", \
                    "autolap", "Beats", "sec", "MaxHeart", "MinHeart", \
                    "InZone", "y4", "Elevation", "Track"]
    point_keys = ["Distance", "Speed", "Time", "Heart", "x1", "InZone", \
                      "Latitude", "Longitude", "kcal", "Elevation", "No", "Track"]
    waypoint_keys = ["Time", "Name", "Latitude", "Longitude","x1","x2","Elevation","No"]
    settings_keys = ["Female", "Age", "Metric", "x3",  "kg", "cm", "zone_active", \
                         "zone1_low",  "zone1_high", "zone2_low", "zone2_high", "zone3_low",\
                         "zone3_high", "zone_alarm", "x5", "Autolap", "Contrast", "x8", "NightMode", \
                         "y2",  "lb", "in", "24hr", "y6", "y7", "y8", "z1", "z2"]

    def __init__(self, dir, hook=None):
        self.dir = dir
        self.hook = hook
        
        self.lapFile = None
        self.lapWriter = None

        self.ptsFile = None
        self.ptsWriter = None

        name = os.path.join(self.dir, "waypoints.csv")
        wptFile = open(name, "wb", **open_extra)
        self.wptWriter = csv.DictWriter(wptFile, self.waypoint_keys)
        self.wptWriter.writeheader()

    def add_track(self, track):
        """ Append track to database """
        name = os.path.join(self.dir, track['Track'])
        trkFile = open('%s.track' % name, "wb", **open_extra)
        trkWriter = csv.DictWriter(trkFile, self.track_keys,extrasaction='ignore')
        trkWriter.writeheader()
        trkWriter.writerow(track)
        trkFile.close()
        
        self.lapFile = open('%s.laps' % name, "wb", **open_extra)
        self.lapWriter = csv.DictWriter(self.lapFile, self.lap_keys,extrasaction='ignore')
        self.lapWriter.writeheader()

        self.ptsFile = open('%s.points' % name, "wb", **open_extra)
        self.ptsWriter = csv.DictWriter(self.ptsFile, self.point_keys)
        self.ptsWriter.writeheader()

        for lap in track['LapData']:
          self.add_lap(lap)

        self.ptsFile.close()
        self.lapFile.close()

    def add_lap(self, lap):
        """ Append lap to a database """
        self.lapWriter.writerow(lap)
        for point in lap['PointData']:
          self.add_point(point)
          
    def add_point(self, point):
        """ Append point to a database """
        self.ptsWriter.writerow(point)

    def add_waypoint(self, wp):
        """ Append point to a database """
        self.wptWriter.writerow(wp)

    def save_settings(self, s):
        name = os.path.join(self.dir, "settings.csv")
        f = open(name, "wb", **open_extra)
        w = csv.DictWriter(f, self.settings_keys)
        w.writeheader()
        w.writerow(s)

if __name__ == '__main__':
    pass
