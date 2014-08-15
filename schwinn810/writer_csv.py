""" Simple CSV writer for Schwinn 810 """

import sys,os
from subprocess import Popen
import csv
import logging

_log = logging.getLogger(__name__)

open_extra = {}
mode = "wb"
if sys.version_info >= (3,0):
    open_extra["newline"] = ''
    mode = "w"

class Writer:
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

    def __init__(self, dir, fmt=".", hook=None):
        self.dir = dir
        self.fmt = fmt
        self.hook = hook
        
        self.lapFile = None
        self.lapWriter = None

        self.ptsFile = None
        self.ptsWriter = None

        name = os.path.join(self.dir, "waypoints.csv")
        wptFile = open(name, mode, **open_extra)
        self.wptWriter = csv.DictWriter(wptFile, self.waypoint_keys)
        self.wptWriter.writeheader()

    def add_track(self, track):
        """ Append track to database """
        name = os.path.join(self.dir, track['Start'].strftime(self.fmt))
        try:
            os.makedirs(name)
        except OSError:
            if not os.path.exists(name):
                raise
        name = os.path.join(name, track['Track'])
        trkFile = open('%s.track' % name, mode, **open_extra)
        trkWriter = csv.DictWriter(trkFile, self.track_keys)
        trkWriter.writeheader()
        trkWriter.writerow(track)
        trkFile.close()
        
        self.lapFile = open('%s.laps' % name, mode, **open_extra)
        self.lapWriter = csv.DictWriter(self.lapFile, self.lap_keys)
        self.lapWriter.writeheader()

    def add_lap(self, lap):
        """ Append lap to a database """
        self.lapWriter.writerow(lap)

    def begin_points(self, summary):
        """ Points for track will follow """
        track = summary['Track']
        if self.lapFile:
            self.lapFile.close()
            self.lapFile = None
        self.track = os.path.join(self.dir, summary['Start'].strftime(self.fmt), track)
        self.ptsFile = open('%s.points' % self.track, mode, **open_extra)
        self.ptsWriter = csv.DictWriter(self.ptsFile, self.point_keys)
        self.ptsWriter.writeheader()

    def add_point(self, point):
        """ Append point to a database """
        self.ptsWriter.writerow(point)

    def commit(self):
        """ Commit last track in a database """
        if self.ptsFile:
            self.ptsFile.close()
            self.ptsFile = None
        if self.hook:
            _log.info("Calling %s\n\twith %s", self.hook, self.track)
            Popen([self.hook, self.track])

    def add_waypoint(self, wp):
        """ Append point to a database """
        self.wptWriter.writerow(wp)

    def save_settings(self, s):
        name = os.path.join(self.dir, "settings.csv")
        f = open(name, mode, **open_extra)
        w = csv.DictWriter(f, self.settings_keys)
        w.writeheader()
        w.writerow(s)

if __name__ == '__main__':
    pass
