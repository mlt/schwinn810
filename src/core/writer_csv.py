""" Simple CSV writer for Schwinn 810 """

import sys,os
import subprocess
import csv
import logging

_log = logging.getLogger(__name__)

open_extra = {}
if sys.version_info >= (3,0):
    open_extra["newline"] = ''

class Writer:
    """ Default files writer """

    track_keys = ["Start", "End", "Laps", "MaxHeart", "Heart", "MaxSpeed", \
                      "Speed", "x4", "x5", "Points", "Track"]
    lap_keys = ["Time", "Speed", "Lap", "Distance", "kcal", "MaxSpeed", \
                    "autolap", "Beats", "sec", "MaxHeart", "MinHeart", \
                    "InZone", "y4", "Elevation", "Track"]
    point_keys = ["Distance", "Speed", "Time", "Heart", "x1", "InZone", \
                      "Latitude", "Longitude", "kcal", "Elevation", "No", "Track"]
    waypoint_keys = ["Timestamp", "Name", "Latitude", "Longitude","x1","x2","Elevation","No"]

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
        trkWriter = csv.DictWriter(trkFile, self.track_keys)
        trkWriter.writeheader()
        trkWriter.writerow(track)
        trkFile.close()
        
        self.lapFile = open('%s.laps' % name, "wb", **open_extra)
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
        self.track = track
        name = os.path.join(self.dir, track)
        self.ptsFile = open('%s.points' % name, "wb", **open_extra)
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
            name = os.path.join(self.dir, self.track)
            _log.info("Calling %s\n\twith %s", self.hook, name)
            subprocess.Popen([self.hook, name])

    def add_waypoint(self, wp):
        """ Append point to a database """
        self.wptWriter.writerow(wp)

    def __del__(self):
        # self.lapFile.close()
        _log.info("Writer destroyed")

if __name__ == '__main__':
    pass
