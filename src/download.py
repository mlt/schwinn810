#!/usr/bin/env python
from __future__ import print_function
import sys,os
import subprocess,stat,tempfile
import argparse
import struct
import csv
import serial
import re
from sys import exit
#from yaml import load, dump

parser = argparse.ArgumentParser(description='Download tracks from Schwinn 810 GPS sport watch with HRM.')
parser.add_argument('--port', nargs=1, dest='port',
                   default=[ {'posix': '/dev/ttyUSB0', 'nt': 'COM5'}[os.name] ],
#                   default=['COM5'] if os.name=='nt' else ['/dev/ttyUSB0'],
                   help='Virtual COM port created by cp201x for Schwinn 810 GPS watch')
parser.add_argument('--hook', nargs=1, dest='hook',
                   help='Callback upon track extraction')
parser.add_argument('--dir', nargs=1, dest='dir',
                   default=['.'],
                   help='Where to store data')
parser.add_argument('--debug', dest='debug', action='store_true',
                    help='Dump all replies in a binary form into a single file schwinn810.bin in TEMP dir')
parser.add_argument('--delete', dest='delete', action='store_true',
                   help='Delete all data from watches after download?')
# parser.add_argument('--add-year', dest='add_year', action='store_true',
#                    help='Creates subfolder in dir named after the current year')
# parser.add_argument('--add-id', dest='add_id', action='store_true',
#                    help='Creates subfolder with device id inside dir but before year')

args = parser.parse_args()

open_extra = dict();
if sys.version_info >= (3,0):
    open_extra["newline"] = ''

connect    = bytearray.fromhex("EEEE000000000000000000000000000000000000000000000000000000000000")
disconnect = bytearray.fromhex("FFFFFFFF00000000000000000000000000000000000000000000000000000000")
download   = bytearray.fromhex("0808AAAA00000000000000000000000000000000000000000000000000000000")
delete     = bytearray.fromhex("000000000000000000000000000000000000000000000000000000000000FFFD")

def unpackBCD(x0):
    x00 = x0
    x = 0
    m = 0
    while x0:
        digit = x0 & 0x000f
        if digit>9:
            raise Exception("Non-BCD argument {:X} in {:X}".format(digit, x00))
        x = x + digit * 10**m
        m = m + 1
        x0 = x0 >> 4
    return x

def pack_coord(c0, hemi):
    c1 = struct.unpack(">HBHs", c0)
    c2=[unpackBCD(x) for x in c1[0:3]]
    c = c2[0] + (c2[1]+c2[2]/10000.)/60.
    if (c1[3] == hemi) : c = -c
    return c

#serial.Serial("COM5", 115200, timeout=20, writeTimeout=20)
reg = False
if os.name != 'nt' or not re.match("com\\d", args.port[0], re.IGNORECASE):
    reg = stat.S_ISREG(os.stat(args.port[0]).st_mode) # is regular file, i.e. previously dumped

if not reg:
    try:
        port = serial.Serial(args.port[0], 115200, timeout=1, writeTimeout=1)
    except serial.SerialException as e:
        print("Port can't be opened :(", file=sys.stderr)
        exit(-1)
    port.write(connect)
else:
    print("Parsing existing dump in {:s}".format(args.port[0]))
    port = open(args.port[0], "rb")

raw = port.read(0x24)
if len(raw)==0:
    print("Did you plug your watches? Check the clip!", file=sys.stderr)
    exit(-1)

if args.debug:
    dump = open(os.path.join(tempfile.gettempdir(), "schwinn810.bin"), mode="wb")
    dump.write(raw)

(ee, e1, e2, e3, bcd1, bcd2, bcd3, serial, v1, v2, check1, check2) = struct.unpack("sBBBBBB6s6s7s2x2I", raw)
if check1 != check2:
    print("0x{:X} != 0x{:X}".format(check1, check2))
#    port.close()
#    print("We are reading something wrong. Are you trying to communicate with another device?", file=sys.stderr)
#    exit(-1)
id = "{0:s} {1:s} {2:s} {3:02d} {4:02d} {5:02d} {6:02d} {7:02d} {8:02d}" \
    .format(serial.decode('ascii'), v1.decode('ascii'), ee.decode('ascii'), e1, e2, e3, unpackBCD(bcd1), unpackBCD(bcd2), unpackBCD(bcd3))
print("Found %s" % id)
if not reg: port.write(download)
raw = port.read(0x24)

if args.debug:
    dump.write(raw)

tracks_with_points = 0

(tracks, waypoints) = struct.unpack("=28xHH4x", raw)
print("We've got %d tracks and %d waypoints to download" % (tracks, waypoints))
for track in range(tracks):
    raw = port.read(0x24)

    if args.debug:
        dump.write(raw)

    (sec1,min1, hr1, dd1, mm1, yr1, laps, \
         speed_max, speed, hrm, x4, pts, \
         x5, name0, ahr, min2, hr2, dd2, mm2, yr2) = \
         struct.unpack(">6BH HHBBH H7sB5B5x", raw)
    tracks_with_points += (pts>0)
    start="20%02d-%02d-%02d %d:%02d:%02d" % (yr1, mm1,dd1, hr1, min1, sec1)
    end="20%02d-%02d-%02d %d:%02d" % (yr2, mm2, dd2, hr2, min2)
    track_name = name0.decode('ascii')
    print("There are %d laps in %s" % (laps-1, track_name))
    name = os.path.join(args.dir[0], track_name)
    trkFile = open('%s.track' % name, "wb", **open_extra)
    trkWriter = csv.writer(trkFile)
    trkWriter.writerow(["Start", "End", "Laps","MaxHeart","Heart","MaxSpeed","Speed","x4","x5","Points","Track"])
    trkWriter.writerow([start, end, laps-1, hrm, ahr, speed_max/10., speed/10., x4, x5, pts, track_name])
    lapFile = open('%s.laps' % name, "wb", **open_extra)
    lapWriter = csv.writer(lapFile)
    lapWriter.writerow(["Time", "Speed", "Lap", "Distance", "kcal", "MaxSpeed", \
                            "autolap", "Beats", "sec", "MaxHeart", "MinHeart", \
                            "InZone", "y4", "Elevation", "y8", "Track"])
    for theLap in range(1,laps):
        raw = port.read(0x24)

        if args.debug:
            dump.write(raw)

        (hh, mm, ss, sss, dist, \
             cal, speed_max, speed, \
             autolap, beats_high, beats_mid, beats_low, sec,heart_max,heart_min, \
             iz_h, iz_m, iz_s, y4, z_low, z_mid, z_high, y8, \
             lap, track, sign) = \
            struct.unpack(">4BI IxBxB 4BH2B 3BB3BB HBB", raw)
        z = z_low | z_mid << 8 | z_high << 16
        time=hh*3600 + mm*60 + ss + sss/100.
        iz = iz_h*3600 + iz_m*60 + iz_s
        lapWriter.writerow([time, speed/10., lap, dist/1e5, cal/1e4, speed_max/10., autolap, \
                                beats_high*65536 + beats_mid*256 + beats_low, \
                                sec, heart_max, heart_min, iz, y4, z/1e2, y8, track_name])
    lapFile.close()
    trkFile.close()

# now all track points
# for tracks containing them only!
for track in range(tracks_with_points):
    raw = port.read(0x24)

    if args.debug:
        dump.write(raw)

    (min1, hr1, dd1, mm1, yr1, laps, hrm, pts, name0, ahr, min2, hr2, dd2, mm2, yr2) = \
        struct.unpack(">x5BH4xBxHxx7sB5B5x", raw)
    track_name = name0.decode('ascii')
    print("Fetching %d points from %s" % (pts, track_name))
    name = os.path.join(args.dir[0], track_name)
    ptsFile = open('%s.points' % name, "wb", **open_extra)
    ptsWriter = csv.writer(ptsFile)
    ptsWriter.writerow(["Distance", "Speed", "Time", "Heart","x1","InZone","Latitude","Longitude","kcal","Elevation","No","Track"])
#    while pts:
    for thePoint in range(pts):
        raw = port.read(0x24)

        if args.debug:
            dump.write(raw)

        (dist, speed0, sec, min, hr, x1, hrm0, izhh, izss, izmm, lat0, lon0, cal, \
             z_low, z_high, pt0, trk, sign) = \
             struct.unpack("=I2s3BB2s3B5s6sH HB3sBB", raw)
        time = "20{:02d}-{:d}-{:d} {:02d}:{:02d}:{:02d}".format(yr1, mm1, dd1, hr, min, sec)
        (hrm) = struct.unpack(">H",hrm0)[0]/5.
        (speed) = struct.unpack(">H",speed0)[0]#/150
        (pt_high, pt_low) = struct.unpack(">BH",pt0)
        pt = pt_low | pt_high << 16
#        (inzone,) = struct.unpack(">H",inzone0)
        lat = pack_coord(b"\x00" + lat0, b'S')
        lon = pack_coord(lon0, b'W')
        inzone = "{:d}:{:d}:{:d}".format(izhh, izmm, izss) # FIXME replace with plain seconds
        ptsWriter.writerow([dist/1e5, speed/160., time, hrm, x1, inzone, lat, lon, cal, \
                                (z_low | z_high << 16)/100., \
                                pt, track_name])
        if pt % 100 == 0:
            print("{:.0f}%".format(100.*pt/pts))
#        pts = pts - 1
    ptsFile.close()
    if args.hook:
        print("Calling {:s}\n\twith {:s}".format(args.hook[0], name))
        subprocess.Popen([args.hook[0], name])

# Waypoints
# TODO make use of waypoints count
name = os.path.join(args.dir[0], "waypoints.csv")
wptWriter = csv.writer(open(name, "wb", **open_extra))
wptWriter.writerow(["Timestamp", "Name", "Latitude", "Longitude","x1","x2","Elevation","No"])
while True:
    raw = port.read(0x24)
    if args.debug:
        dump.write(raw)
    if raw[0:2] == b"\xee\xee":
        break
    (yy, mm, dd, hh, mn, ss, name0, lat0, lon0, x1,x2, z, num, sign) = \
        struct.unpack("=6B6s3x5s6s2BH4xBB", raw)
    time = "{:2d}/{:2d}/{:2d} {:2d}:{:02d}:{:02d}".format(mm,dd,yy,hh,mn,ss)
    name = name0.decode('ascii')
    lat = pack_coord(b"\x00" + lat0, b'S')
    lon = pack_coord(lon0, b'W')
    wptWriter.writerow([time, name, lat, lon, x1, x2, z/100., num])

if not reg and args.delete:
    if args.debug:
        port.write(delete)
    else:
        print("--debug is required for deletion for now", file=sys.stderr)

if args.debug:
    dump.close()

if not reg: port.write(disconnect)
port.close()

print("Done")
