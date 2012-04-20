#!/usr/bin/python3.2
# This script converts lap and point data into TCX history

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
    track_start = tz.localize(datetime.strptime(track["Start"], "%Y-%m-%d %H:%M"))
#    e = datetime.strptime(track["End"], "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    print("""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd">
    
        <Activities>
            <Activity Sport="Running">
                <Id>{:s}</Id>""".format(track_start.isoformat()))
    lap_start = track_start
    prev = 0.

    with open(base+".laps") as l, open(base+".points") as p:
        laps = DictReader(l)
        points = DictReader(p)
        thePoint = next(points)
        for theLap in laps:
            print("""                    <Lap StartTime="{:s}">
                        <TotalTimeSeconds>{:f}</TotalTimeSeconds>
                        <DistanceMeters>{:f}</DistanceMeters>
                        <MaximumSpeed>{:s}</MaximumSpeed>
                        <Calories>{:d}</Calories>
                        <Intensity>Active</Intensity>
                        <TriggerMethod>Location</TriggerMethod>
                        <Track>""".format(lap_start.isoformat(), \
                                              float(theLap["Time"])-prev, \
                                              float(theLap["Distance"])*1.e3, \
                                              theLap["MaxSpeed"], \
                                              round(float(theLap["kcal"]))))
            lap_start = track_start + timedelta(seconds=float(theLap["Time"]))
            prev = float(theLap["Time"])

            while True:
                time = tz.localize(datetime.strptime(thePoint["Time"], "%Y-%m-%d %H:%M:%S"))
                if time > lap_start:
                    break
                print("""                            <Trackpoint>
                                    <Time>{:s}</Time>
                                    <Position>
                                        <LatitudeDegrees>{:s}</LatitudeDegrees>
                                        <LongitudeDegrees>{:s}</LongitudeDegrees>
                                    </Position>
                                    <AltitudeMeters>{:s}</AltitudeMeters>
                                    <DistanceMeters>{:f}</DistanceMeters>""".format(time.isoformat(), \
                                                        thePoint["Latitude"], \
                                                        thePoint["Longitude"], \
                                                        thePoint["Elevation"], \
                                                        float(thePoint["Distance"])*1.e3))
                heart = round(float(thePoint["Heart"]))
                if heart > 0:
                    print("""                                    <HeartRateBpm><Value>{:d}</Value></HeartRateBpm>
                                    <SensorState>Present</SensorState>""".format(heart))
                else:
                    print("                                    <SensorState>Absent</SensorState>")

                print("                            </Trackpoint>")

                try:
                    thePoint = next(points)
                except StopIteration:
                    break

            print("""                        </Track>
                    </Lap>""")

    print("""            </Activity>
        </Activities>

</TrainingCenterDatabase>""")
