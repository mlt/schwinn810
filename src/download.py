#!/usr/bin/python3.2
import argparse
import struct
import csv
import serial
from time import sleep
#from yaml import load, dump

parser = argparse.ArgumentParser(description='Download tracks from Schwinn 810 GPS sport watches with HRM.')
parser.add_argument('--port', nargs=1, dest='port',# action='store_const',const='/dev/ttyUSB0', 
                   default='/dev/ttyUSB0', #required=True,
                   help='Virtual COM port created by cp201x for Schwinn 810 watches')
parser.add_argument('--delete', dest='delete', action='store_true',
                   help='Delete all data from watches after download?')

args = parser.parse_args()

connect    = bytes.fromhex("EEEE000000000000000000000000000000000000000000000000000000000000")
disconnect = bytes.fromhex("FFFFFFFF00000000000000000000000000000000000000000000000000000000")
download   = bytes.fromhex("0808AAAA00000000000000000000000000000000000000000000000000000000")
delete     = bytes.fromhex("000000000000000000000000000000000000000000000000000000000000FFFD")

def unpackBCD(x0):
    x = 0
    m = 0
    while x0:
        digit = x0 & 0x000f
        x = x + digit * 10**m
        m = m + 1
        x0 = x0 >> 4
    return x

def pack_coord(c0, hemi):
    c1 = struct.unpack(">H3Bs", c0)
    c2=[unpackBCD(x) for x in c1[0:4]]
    c = c2[0] + c2[1]/60 + (c2[2] + c2[3]/100)/3600
    if (c1[4] == hemi) : c = -c
    return c

#serial.Serial("COM5", 115200, timeout=20, writeTimeout=20)
port = serial.Serial("/dev/ttyUSB0", 115200) #, timeout=50, writeTimeout=50)
port.open()
port.write(connect)
raw = port.read(0x24)
(ee, e1, e2, e3, bcd1, bcd2, bcd3, serial, v1, v2, check1, check2) = struct.unpack("sBBBBBB6s5s8s2x2I", raw)
## check1 == check2
#q = "%s %s %s %02d %02d %02d %02d %02d %02d" % (serial, v1, ee, e1, e2, e3, unpackBCD(bcd1), unpackBCD(bcd2), unpackBCD(bcd3))
id = "{0:s} {1:s} {2:s} {3:02d} {4:02d} {5:02d} {6:02d} {7:02d} {8:02d}" \
    .format(serial.decode('ascii'), v1.decode('ascii'), ee.decode('ascii'), e1, e2, e3, unpackBCD(bcd1), unpackBCD(bcd2), unpackBCD(bcd3))
print("Found %s" % id)
port.write(download)
raw = port.read(0x24)
(tracks,) = struct.unpack("=28xH6x", raw)
print("We've got %d tracks" % tracks)
for track in range(tracks):
    raw = port.read(0x24)
    (x1,min1, hr1, dd1, mm1, yr1, laps, x2, x3, hrm, avspd, pts, x5, name0, ahr, min2, hr2, dd2, mm2, yr2) = \
        struct.unpack(">B5BHHHBBHH7sB5B5x", raw)
    start="%02d/%02d/%02d %d:%d" % (mm1,dd1,yr1, hr1,min1)
    end="%02d/%02d/%02d %d:%d" % (mm2,dd2,yr2, hr2,min2)
    name = name0.decode('ascii')
    print("There are %d laps in %s" % (laps-1, name))
    trkWriter = csv.writer(open('%s.track' % name, 'w'))
    trkWriter.writerow(["Start", "End", "Laps","MaxPulse","AveragePulse","x1","x2","x3","AvSpeed","x5"])
    trkWriter.writerow([start, end, laps, hrm, ahr, x1, x2, x3, avsp, x5])
    lapWriter = csv.writer(open('%s.laps' % name, 'w'))
    lapWriter.writerow(["Time", "Speed", "Lap","x1","x2","x3","x4","x5","x6","x7","x8", "Speed2","y1","y2","y3","y4","y5","y6","y7","y8"])
    for theLap in range(1,laps):
        raw = port.read(0x24)
        (hh, mm, ss, sss, x1,x2,x3,x4,x5,x6,x7,x8,speed2, speed, y1,y2,y3,y4,y5,y6,y7,y8,lap, track, sign) = \
            struct.unpack(">4B8BxBxB8x4B4BHBB", raw)
        time=hh*3600 + mm*60 + ss + sss/100
        lapWriter.writerow([time, speed/10, lap,x1,x2,x3,x4,x5,x6,x7,x8,speed2,y1,y2,y3,y4,y5,y6,y7,y8])

# now all track points
for track in range(tracks):
    raw = port.read(0x24)
    (min1, hr1, dd1, mm1, yr1, laps, hrm, pts, name0, ahr, min2, hr2, dd2, mm2, yr2) = \
        struct.unpack(">x5BH4xBxHxx7sB5B5x", raw)
    name = name0.decode('ascii')
    print("Fetching %d points from %s" % (pts, name))
    ptsWriter = csv.writer(open('%s.points' % name, 'w'))
    ptsWriter.writerow(["Distance", "Speed", "Time", "Pulse","x1","InZone","Latitude","Longitude","Cal","Elevation","Point"])
    while pts:
        raw = port.read(0x24)
        (dist, speed0, time, x1, hrm0, inzone0, lat0, lon0, cal, z, pt0, trk, sign) = \
            struct.unpack("=I2sHH2s2s6s6sHH4sBB", raw)
        (hrm) = struct.unpack(">H",hrm0)[0]/5
        (speed) = struct.unpack(">H",speed0)[0]#/150
        (pt,) = struct.unpack(">I",pt0)
        (inzone,) = struct.unpack(">H",inzone0)
        lat = pack_coord(lat0, b'S')
        lon = pack_coord(lon0, b'W')
        ptsWriter.writerow([dist/100, speed, time, hrm, x1, inzone, lat, lon, cal, z/100, pt])
        pts = pts - 1

last = port.read()
port.write(disconnect)
port.close()

print("Done")
