#!/usr/bin/env python
# This script converts lap and point data into TCX history

from __future__ import print_function
import argparse, os
from csv import DictReader
from pytz import timezone, utc
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='Create TCX from lap & point data')
parser.add_argument('--tz', nargs=1, dest='tz',
                   default=[ 'America/Chicago' ],
                   help='Local time zone')
parser.add_argument(dest='path',
                   help='Path to track data')

args = parser.parse_args()

tz = timezone(args.tz[0])
base = os.path.splitext(args.path)[0]
tcx_name = base + ".tcx"

with open(base+".track") as t:
    track = next(DictReader(t))
    try:
        track_start = tz.localize(datetime.strptime(track["Start"], "%Y-%m-%d %H:%M:%S"))
    except:                     # support for legacy format with standalone x1
        track_start = tz.localize(datetime.strptime("{:s}:{:s}".format(track["Start"], track["x1"]), "%Y-%m-%d %H:%M:%S"))

#    e = datetime.strptime(track["End"], "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    print("""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd">

 <Activities>
  <Activity Sport="Running">
   <Id>{:s}</Id>""".format(track_start.astimezone(utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    lap_start = track_start
    time_prev = 0.
    kcal_prev = 0
    dist_prev = 0.
    beats_prev = 0

    with open(base+".laps") as l, open(base+".points") as p:
        laps = DictReader(l)
        points = DictReader(p)
        thePoint = next(points)
        for theLap in laps:
            time = float(theLap["Time"])
            kcal = int(float(theLap["kcal"]))
            lap_dist = float(theLap["Distance"])*1.e3
            beats = int(theLap["Beats"])
            print("""   <Lap StartTime="{:s}">
    <TotalTimeSeconds>{:f}</TotalTimeSeconds>
    <DistanceMeters>{:f}</DistanceMeters>
    <MaximumSpeed>{:s}</MaximumSpeed>
    <Calories>{:d}</Calories>
    <AverageHeartRateBpm><Value>{:d}</Value></AverageHeartRateBpm>""".format(lap_start.astimezone(utc).strftime("%Y-%m-%dT%H:%M:%SZ"), \
                                                                                 time - time_prev, \
                                                                                 lap_dist - dist_prev, \
                                                                                 theLap["MaxSpeed"], \
                                                                                 kcal - kcal_prev, \
                                                                                 int((beats - beats_prev)/(time - time_prev))))
            time_prev = time
            kcal_prev = kcal
            dist_prev = lap_dist
            beats_prev = beats
            heart_max = int(theLap["MaxHeart"])
            if heart_max>0:
                print("""    <MaximumHeartRateBpm><Value>{:d}</Value></MaximumHeartRateBpm>""".format(heart_max))
            print("""    <Intensity>Active</Intensity>
    <TriggerMethod>Location</TriggerMethod>
    <Track>""")

            while True:
                time = tz.localize(datetime.strptime(thePoint["Time"], "%Y-%m-%d %H:%M:%S"))
                dist = float(thePoint["Distance"])*1.e3
                if dist > lap_dist: # the only reliable next lap criteria
                    lap_start = time # the only source of absolute time
                    break
                print("""     <Trackpoint>
      <Time>{:s}</Time>
      <Position>
       <LatitudeDegrees>{:0.6f}</LatitudeDegrees>
       <LongitudeDegrees>{:0.6f}</LongitudeDegrees>
      </Position>
      <DistanceMeters>{:f}</DistanceMeters>""".format(time.astimezone(utc).strftime("%Y-%m-%dT%H:%M:%SZ"), \
                                                          float(thePoint["Latitude"]), \
                                                          float(thePoint["Longitude"]), \
                                                          dist))
                if thePoint['Elevation']:
                    print("""      <AltitudeMeters>{:s}</AltitudeMeters>""".format(
                            thePoint["Elevation"]))
                heart = int(float(thePoint["Heart"]))
                if heart > 0:
                    print("""      <HeartRateBpm><Value>{:d}</Value></HeartRateBpm>
      <SensorState>Present</SensorState>""".format(heart))
                else:
                    print("      <SensorState>Absent</SensorState>")

                print("     </Trackpoint>")

                try:
                    thePoint = next(points)
                except StopIteration:
                    break

            print("""    </Track>
   </Lap>""")

    print("""
   <Creator xsi:type="Device_t">
    <Name>Schwinn 810 GPS</Name>
    <UnitId>2882</UnitId>
    <ProductID>11153</ProductID>
    <Version>
     <VersionMajor>1</VersionMajor>
     <VersionMinor>20</VersionMinor>
     <BuildMajor>0</BuildMajor>
     <BuildMinor>0</BuildMinor>
    </Version>
   </Creator>
  </Activity>
 </Activities>

</TrainingCenterDatabase>""")
