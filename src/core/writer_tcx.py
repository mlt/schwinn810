""" Simple CSV writer for Schwinn 810 """

from __future__ import print_function
import sys,os
import subprocess
import csv
import logging
from writer import *
from pytz import timezone, utc
from datetime import datetime, timedelta

_log = logging.getLogger(__name__)

tz = utc #timezone("UTC")

open_extra = {}
if sys.version_info >= (3,0):
    open_extra["newline"] = ''

class WriterTCX(Writer):
    """ TCX files writer """

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
        self.tracks_processed = []

        #name = os.path.join(self.dir, "waypoints.csv")
        #wptFile = open(name, "wb", **open_extra)
        #self.wptWriter = csv.DictWriter(wptFile, self.waypoint_keys)
        #self.wptWriter.writeheader()

    def output(self, text):
        print(text, file=self.trkFile)

    def add_track(self, track):
        """ Append track to database """
        name = os.path.join(self.dir, '%s.tcx' % track['Track'])
        track['Filename'] = name
        self.trkFile = open(name, "wb", **open_extra)
        self.open_track(track)

        for lap in track['LapData']:
          self.add_lap(lap)

        self.close_track()
        self.trkFile.close()

        self.tracks_processed.append(track)


    def open_track(self, track):
        track_start = track["Start"]
        self.output("""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd">

 <Activities>
  <Activity Sport="Running">
   <Id>{:s}</Id>""".format(track_start.strftime("%Y-%m-%dT%H:%M:%SZ")))



    def open_lap(self, lap):
            """ Add a lap to the tcx file """
            time = float(lap["Time"])
            kcal = int(float(lap["kcal"]))
            lap_dist = float(lap["Distance"])*1.e3
            beats = int(lap["Beats"])
            try:
              lap_start = lap['Start'].strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception as e:
              print(lap)
              raise e
              
            duration_secs = lap['DurationSecs']
            
            self.output("""   <Lap StartTime="{:s}">
    <TotalTimeSeconds>{:f}</TotalTimeSeconds>
    <DistanceMeters>{:f}</DistanceMeters>
    <MaximumSpeed>{:0.1f}</MaximumSpeed>
    <Calories>{:d}</Calories>
    <AverageHeartRateBpm><Value>{:d}</Value></AverageHeartRateBpm>""".format(lap_start, \
                                                                                 duration_secs, \
                                                                                 lap['LengthMeters'], \
                                                                                 lap["MaxSpeed"], \
                                                                                 int(lap['kcalDelta']), \
                                                                                 int(lap['BeatsDelta']/(duration_secs))))
            heart_max = int(lap["MaxHeart"])
            if heart_max>0:
                self.output("""    <MaximumHeartRateBpm><Value>{:d}</Value></MaximumHeartRateBpm>""".format(heart_max))
            self.output("""    <Intensity>Active</Intensity>
    <TriggerMethod>Location</TriggerMethod>
    <Track>""")

    def add_lap(self, lap):
        _log.debug("writing lap with {:d} points".format(len(lap['PointData'])))
        self.open_lap(lap)
        for point in lap['PointData']:
          self.add_point(point, lap)
        self.close_lap()

    def add_point(self, point, parent_lap):
                """ Append point to a open lap """
                time = tz.localize(point["Time"])
                dist = float(point["Distance"])*1.e3
                self.output("""     <Trackpoint>
      <Time>{:s}</Time>
      <Position>
       <LatitudeDegrees>{:f}</LatitudeDegrees>
       <LongitudeDegrees>{:f}</LongitudeDegrees>
      </Position>
      <DistanceMeters>{:f}</DistanceMeters>""".format(time.astimezone(utc).strftime("%Y-%m-%dT%H:%M:%SZ"), \
                                                          point["Latitude"], \
                                                          point["Longitude"], \
                                                          dist))
                if parent_lap['HasElevation']:
                    self.output("""      <AltitudeMeters>{:d}</AltitudeMeters>""".format(int(point["Elevation"])))
                heart = int(float(point["Heart"]))
                if heart > 0:
                    self.output("""      <HeartRateBpm><Value>{:d}</Value></HeartRateBpm>
      <SensorState>Present</SensorState>""".format(heart))
                else:
                    self.output("      <SensorState>Absent</SensorState>")

                self.output("     </Trackpoint>")

    def close_lap(self):
        """ Add the </..> tags to close the lap """
        self.output("    </Track>")
        self.output("   </Lap>")

    def close_track(self):
        """ Add the </..> tags to close the track """
        self.output("</Activity>")
        self.output("</Activities>")
        self.output("</TrainingCenterDatabase>")

    def add_waypoint(self, wp):
        """ Append point to a database """
        # do nowt
        

    def save_settings(self, s):
        name = os.path.join(self.dir, "settings.csv")
        f = open(name, "wb", **open_extra)
        w = csv.DictWriter(f, self.settings_keys)
        w.writeheader()
        w.writerow(s)

    def tracks_written(self):
        return self.tracks_processed

if __name__ == '__main__':
    pass
