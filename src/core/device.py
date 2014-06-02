""" Module with device class to communicate with Schwinn 810 """

from __future__ import print_function
import os, re, stat, tempfile
import struct
if 'nt' == os.name:
    from pyusbxp import Usbxp, UsbxpError as SerialException
else:
    from serial import Serial, SerialException
from commands import *
from utils import unpack_bcd
import logging
# from collections import namedtuple
from datetime import datetime, timedelta
from reader_schwinn import SchwinnReader
from reader_cresta import CrestaReader

_log = logging.getLogger(__name__)

class NotConnected(Exception): pass

class Device:
    """ Device class to communicate with Schwinn 810 """

    def __init__(self, device=None, debug=False):
        self.device = device
        self._debug = debug
        self.dump = False       # are we reading previously backed up dump?
        self.connected = False
        self.port = None        # device handle
        self.reader = None      # device specific data chunk parser
        self.backup = None      # backup file handle
        self.shift = None       # fix for incorrect TZ set on watch
        if self.device:
            self.open()

    def open(self, device=None):
        """ Open port or existing dump """
        if self.port:
            return
        if device:
            self.device = device
        if os.name != 'nt' or not re.match("com\\d", self.device, re.IGNORECASE):
            try:
                self.dump = stat.S_ISREG(os.stat(self.device).st_mode) # is regular file, i.e. previously dumped
            except OSError as e:
                pass
        if not self.dump:
            if 'nt' == os.name:
                self.port = Usbxp()#dbg=True)
                self.port.open()
                self.port.setbr(115200)
            else:
                self.port = Serial(self.device, 115200, timeout=1, writeTimeout=1)
        else:
            _log.warn("Parsing existing dump in {:s}".format(self.device))
            self.port = open(self.device, "rb")
        self.connect()

    def connect(self):
        """ Issue connect command and set up a reader"""
        if self.connected:
            return
        if not self.dump:
            self.port.write(CONNECT)

        raw = self.port.read(0x20)
        if len(raw)==0:
            _log.fatal("Did you plug your watches? Check the clip!")
            raise NotConnected()
        else:
            self.connected = True

        if self._debug:
            self.backup = open(os.path.join(tempfile.gettempdir(), "schwinn810.bin"), mode="wb")
            self.backup.write(raw)

        (ee, e1, e2, e3, bcd1, bcd2, bcd3, serial, v1, v2, sign1) = struct.unpack("sBBBBBB6s6s7s2xI", raw)
        if sign1:               # 0x0130ff00
            raw = self.port.read(4)
            if self._debug:
                self.backup.write(raw)
            (sign2,) = struct.unpack("I", raw)
            if sign1 != sign2:
                print("0x{:X} != 0x{:X}".format(sign1, sign2))
                # port.close()
                # print("We are reading something wrong. Are you trying to communicate with another device?", file=sys.stderr)
                # exit(-1)
            self.reader = SchwinnReader(self.port, self.backup)
        else:   # Cresta/Mio
            self.reader = CrestaReader(self.port, self.backup)
            _log.warn("File a bug if you are not using Cresta or Mio watch!")
        id = "{0:s} {1:s} {2:s} {3:02d} {4:02d} {5:02d} {6:02d} {7:02d} {8:02d}" \
            .format(serial.decode('ascii'), v1.decode('ascii'), ee.decode('ascii'), \
                        e1, e2, e3, unpack_bcd(bcd1), unpack_bcd(bcd2), unpack_bcd(bcd3))
        _log.info("Found %s" % id)

    def _read_tracks(self, writer, count):
        tracks_with_points = []
        for i in range(count):
            track = self.reader.read_track()
            if (track['Points']>0):
                tracks_with_points += (track, )
            _log.info("There are %d laps in %s" % (track['Laps'], track['Track']))
            # _log.debug("Testing", extra = track)

            if self.shift:
                track['Start'] += self.shift
                if 'End' in track:
                    track['End'] += self.shift
            writer.add_track(track)

            for j in range(track['Laps']):
                lap = self.reader.read_lap()
                lap['Track'] = track['Track']
                # _log.debug("Lap={:d}, Beats={:d}, Elevation={:f}".format(lap['Lap'], lap['Beats'], lap['Elevation']))
                writer.add_lap(lap)
        return tracks_with_points

    def read(self, writer, progress=None):
        if not self.dump:
            self.port.write(READ)

        summary = self.reader.read_summary()
        tracks = summary['Tracks']
        waypoints = summary['Waypoints']
        # (tracks, waypoints) = self.reader.read_summary()
        _log.info("We've got %d tracks and %d waypoints to download" % (tracks, waypoints))

        tracks_with_points = self._read_tracks(writer, tracks)

        # now all track points
        # for tracks containing them only!
        track_no = 0
        for track in tracks_with_points:
            track_no += 1
            # if isinstance(self.reader, SchwinnReader):
            summary_dummy = self.reader.read_points_summary()
            _log.info("Fetching %d points from %s" % (track['Points'], track['Track']))
            if progress:
                progress.track(track['Track'], track_no, len(tracks_with_points), track['Points'])
            writer.begin_points(track)

            for thePoint in range(track['Points']):
                if progress:
                    progress.point(thePoint, track['Points'])
                point = self.reader.read_point()
                if point:
                    point['Track'] = track['Track']
                    point['Time'] = datetime.combine(track['Start'].date(), point['Time'])
                    if track['Start'] > point['Time']:
                        point['Time'] += timedelta(days=1)
                    if self.shift:
                        point['Time'] += self.shift
                    writer.add_point(point)
            writer.commit()

        for wp in range(waypoints):
            wpt = self.reader.read_waypoint()
            writer.add_waypoint(wpt)

        self.reader.read_end()

    def read_settings(self, writer):
        if not self.dump:
            self.port.write(READ_SETTINGS)

        s = self.reader.read_settings()
        writer.save_settings(s)

    def clear(self):
        if not self.dump and self._debug:
            self.port.write(DELETE)
            self.reader.read_end()
        else:
            _log.warn("Debug is required for deletion for now")

    def close(self):
        if self._debug:
            self.backup.close()

        if not self.dump:
            self.port.write(DISCONNECT)
            self.port.read(1)
        self.port.close()

if __name__ == '__main__':
    pass
