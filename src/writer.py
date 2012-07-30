""" Simple CSV writer for Schwinn 810 """

from __future__ import print_function
import sys,os
import subprocess
import csv
import logging

_log = logging.getLogger(__name__)

open_extra = dict();
if sys.version_info >= (3,0):
    open_extra["newline"] = ''

class Writer:
    """ Default files writer """

    def __init__(self, dir, hook=None):
        self.dir = dir
        self.hook = hook

        self.ptsWriters = {}
        self.pts_count = {}

        name = os.path.join(self.dir, "waypoints.csv")
        wptFile = open(name, "wb", **open_extra)
        waypoint_keys = ["Timestamp", "Name", "Latitude", "Longitude","x1","x2","Elevation","No"]
        self.wptWriter = csv.DictWriter(wptFile, waypoint_keys)
        self.wptWriter.writeheader()

    def add_track(self, track):
        """ Append track to database """
        name = os.path.join(self.dir, track['Track'])
        trkFile = open('%s.track' % name, "wb", **open_extra)
        track_keys = ["Start", "End", "Laps", "MaxHeart", "Heart", "MaxSpeed", \
                          "Speed", "x4", "x5", "Points", "Track"]
        trkWriter = csv.DictWriter(trkFile, track_keys)
        trkWriter.writeheader()
        trkWriter.writerow(track)
        trkFile.close()
        
        lapFile = open('%s.laps' % name, "wb", **open_extra)
        lap_keys = ["Time", "Speed", "Lap", "Distance", "kcal", "MaxSpeed", \
                        "autolap", "Beats", "sec", "MaxHeart", "MinHeart", \
                        "InZone", "y4", "Elevation", "Track"]
        self.lapWriter = csv.DictWriter(lapFile, lap_keys)
        self.lapWriter.writeheader()

        point_keys = ["Distance", "Speed", "Time", "Heart", "x1", "InZone", \
                          "Latitude", "Longitude", "kcal", "Elevation", "No", "Track"]
        if track['Points']>0:
            ptsFile = open('%s.points' % name, "wb", **open_extra)
            ptsWriter = csv.DictWriter(ptsFile, point_keys)
            ptsWriter.writeheader()
            name = track['Track']
            self.ptsWriters[name] = ptsWriter
            self.pts_count[name] = track['Points']

    def add_lap(self, lap):
        """ Append lap to a database """
        self.lapWriter.writerow(lap)

    def begin_points(self, track):
        """ Points for track will follow """
        self.track = track

    def add_point(self, point):
        """ Append point to a database """
        self.ptsWriters[self.track].writerow(point)

    def add_waypoint(self, wp):
        """ Append point to a database """
        self.wptWriter.writerow(wp)

    def commit(self):
        """ Commit last track in a database """
        if self.hook:
            name = os.path.join(self.dir, self.track)
            _log.info("Calling %s\n\twith %s", self.hook, name)
            subprocess.Popen([self.hook, name])

    def __del__(self):
        # self.lapFile.close()
        _log.info("Writer destroyed")

if __name__ == '__main__':
    pass
