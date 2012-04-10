#!/usr/bin/python3.2
import sys,os
import subprocess,stat,tempfile
import argparse
import struct
import csv
import serial
import re
from sys import exit
#from yaml import load, dump

parser = argparse.ArgumentParser(description='Download tracks from Schwinn 810 GPS sport watches with HRM.')
parser.add_argument('--port', nargs=1, dest='port',
                   default=[ {'posix': '/dev/ttyUSB0', 'nt': 'COM5'}[os.name] ],
#                   default=['COM5'] if os.name=='nt' else ['/dev/ttyUSB0'],
                   help='Virtual COM port created by cp201x for Schwinn 810 watches')
parser.add_argument('--hook', nargs=1, dest='hook',
                   help='Callback upon track extraction')
parser.add_argument('--dir', nargs=1, dest='dir',
                   default=['.'],
                   help='Where to store data')
parser.add_argument('--debug', dest='debug', action='store_true',
                    help='Dump all replies in a binary form into a single file schwinn810.bin in TEMP dir')
parser.add_argument('--save', dest='save', action='store_true',
                    help='Save settings')
# parser.add_argument('--delete', dest='delete', action='store_true',
#                    help='Delete all data from watches after download?')
# parser.add_argument('--add-year', dest='add_year', action='store_true',
#                    help='Creates subfolder in dir named after the current year')
# parser.add_argument('--add-id', dest='add_id', action='store_true',
#                    help='Creates subfolder with device id inside dir but before year')

args = parser.parse_args()

connect    = bytes.fromhex("EEEE000000000000000000000000000000000000000000000000000000000000")
disconnect = bytes.fromhex("FFFFFFFF00000000000000000000000000000000000000000000000000000000")
settings_read = bytes.fromhex("000000000000000000000000000000000000000000000000000000000000EEEE")

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

if os.name != 'nt' or not re.match("com\\d", args.port[0], re.IGNORECASE):
    reg = stat.S_ISREG(os.stat(args.port[0]).st_mode) # is regular file, i.e. previously dumped

if not reg:
    try:
        port = serial.Serial(args.port[0], 115200, timeout=1, writeTimeout=1)
        port.open()
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

if args.save:
    pass
else:
    if not reg: port.write(settings_read)
    raw = port.read(0x24)

    if args.debug:
        dump.write(raw)

    (female, age, x2, x3,  kg, cm, zone_active, zone1_low,  zone1_high, zone2_low, zone2_high, zone3_low,\
         zone3_high, zone_alarm, x5, x6,  contrast, x8, night_mode, y2,  y3, y4, hr24, y6, y7, y8, z1, z2, check1, check2) = struct.unpack("=28B2I", raw)
    # contrast 8 => 50%
    # x5=alert
    name = os.path.join(args.dir[0], "settings.csv")
    setFile = open(name, 'w', newline='')
    setWriter = csv.writer(setFile)
    setWriter.writerow(["female", "age", "x2", "x3",  "kg", "cm", "zone_active", "zone1_low",  "zone1_high", "zone2_low", "zone2_high", "zone3_low",\
         "zone3_high", "zone_alarm", "x5", "x6",  "contrast", "x8", "night_mode", "y2",  "y3", "y4", "24hr", "y6", "y7", "y8", "z1", "z2", "check1", "check2"])
    setWriter.writerow([female, age, x2, x3,  kg, cm, zone_active, zone1_low,  zone1_high, zone2_low, zone2_high, zone3_low,\
         zone3_high, zone_alarm, x5, x6,  contrast, x8, night_mode, y2,  y3, y4, hr24, y6,  y7, y8, z1, z2, check1, check2])

if args.debug:
    dump.close()

if not reg: port.write(disconnect)
port.close()

print("Done")
