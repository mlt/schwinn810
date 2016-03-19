""" Module with device class to communicate with Schwinn 810 """

from __future__ import print_function
import os, re, stat, tempfile
import struct
from serial import Serial, SerialException
from commands import *
from utils import unpack_bcd
import logging
# from collections import namedtuple
from datetime import datetime, timedelta
from reader_schwinn import SchwinnReader
from reader_soleus import SoleusReader
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
            self.port.write(SOLEUS_DISCONNECT)
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
        _log.debug("read header")
        _log.debug("{:s} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} {:s} {:s} {:s} 0x{:x}".format(ee, e1, e2, e3, bcd1, bcd2, bcd3, serial, v1, v2, sign1))
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
            if sign1 == 0x243601:  #kb: think maybe we need something else to identify soleus.  This might be specific to my watch.  Perhaps the M11165 string?
              self.reader = SoleusReader(self.port, self.backup)
            else:
              self.reader = SchwinnReader(self.port, self.backup)
        else:   # Cresta/Mio
            self.reader = CrestaReader(self.port, self.backup)
            _log.warn("File a bug if you are not using Cresta or Mio watch!")
        id = "{0:s} {1:s} {2:s} {3:02d} {4:02d} {5:02d} {6:02d} {7:02d} {8:02d}" \
            .format(serial.decode('ascii'), v1.decode('ascii'), ee.decode('ascii'), \
                        e1, e2, e3, unpack_bcd(bcd1), unpack_bcd(bcd2), unpack_bcd(bcd3))
        _log.info("Found %s" % id)

    def _read_tracks(self, count):
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

            track['LapData'] = []
            track['Distance'] = 0
            previous_lap = {'Time' : 0, 'Distance' : 0, 'kcal': 0, 'Beats' : 0}
            for j in range(track['Laps']):
                lap = self.reader.read_lap()
                track['Distance'] = lap['Distance']
                lap['Track'] = track['Track']
                _log.debug("Lap={:d}, Beats={:d}, Elevation={:f}".format(lap['Lap'], lap['Beats'], lap['Elevation']))
                lap['PointData'] = []
                lap['DurationSecs'] = lap['Time'] - previous_lap['Time']
                lap['LengthMeters'] = (lap['Distance'] - previous_lap['Distance'])*1e3
                lap['kcalDelta'] = (lap['kcal'] - previous_lap['kcal'])
                lap['BeatsDelta'] = (lap['Beats'] - previous_lap['Beats'])
                previous_lap = lap
                
                track['LapData'].append(lap)
        return tracks_with_points

    def read(self, writer, progress=None):
        if not self.dump:
            self.port.write(READ)

        summary = self.reader.read_summary()
        tracks = summary['Tracks']
        waypoints = summary['Waypoints']
        # (tracks, waypoints) = self.reader.read_summary()
        _log.info("We've got %d tracks and %d waypoints to download" % (tracks, waypoints))

        tracks_with_points = self._read_tracks(tracks)



        # now all track points
        # for tracks containing them only!
        track_no = 1
        for track in tracks_with_points:
            #chosen = False
            _log.debug("reading track %d" % track_no)
            start = datetime.now()
            #if track_no in chosentracks:
            #  chosen = True
            #track = tracks_with_points[track_no]
            #for lapinfo in track['LapData']:
            current_lap_index = 0  #track['LapData'][0]
            current_lap = track['LapData'][0]
            current_lap_end = track['LapData'][0]['Distance']
            current_lap['Start'] = track['Start']

            # if isinstance(self.reader, SchwinnReader):
            summary_dummy = self.reader.read_points_summary()
            _log.info("Fetching %d points from %s" % (track['Points'], track['Track']))
            _log.debug("Adding points to first lap: {:s}".format(str(current_lap)))
            if progress:
                progress.track(track['Track'], track_no, len(tracks_with_points), track['Points'])
  
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
                      #making this a while loop rather than an if statement skips over laps with zero points in them.
                      while(point['Distance'] > current_lap_end):
                          current_lap_index += 1
                          current_lap = track['LapData'][current_lap_index]
                          current_lap_end = current_lap['Distance']
                          current_lap['Start'] = point['Time']
                          _log.debug("switch to lap: %s at point distance %f" % (str(current_lap), point['Distance']))
                      if(point['Elevation'] > 0):
                          current_lap['HasElevation'] = True
                      current_lap['PointData'].append(point)

            #if there are laps we haven't read points for then presumably they have no points.  Set the start time to the time of the last point
            while current_lap_index < len(track['LapData']) - 1:
              current_lap_index += 1
              track['LapData'][current_lap_index]['Start'] = point['Time']
              

            writer.add_track(track)
            #else:
              #summary_dummy = self.reader.read_points_summary()
              #bytesize = 0x24 * track['Points']
              #_log.debug("skipping %d points = %d bytes from track %d" % (track['Points'], bytesize, track_no))
              #raw = self.reader.read(bytesize)
            track_no += 1
            end = datetime.now()
            _log.debug("finished points for track %d in %d s" % (track_no, (end - start).total_seconds()))

        for wp in range(waypoints):
            wpt = self.reader.read_waypoint()
            writer.add_waypoint(wpt)

        self.reader.read_end()

        #print("Track#\tStarted At\t\tDur.\tSpeed\t\tLaps\tPoints\tDistance")
        #n = 1
        #for twp in tracks_with_points:
          #print("%s\t%s\t%s\t%.1fkm/h\t%d\t%d\t%.2fkm" % (twp['Track'], twp['Start'], twp['End'] - twp['Start'], twp['Speed'], twp['Laps'], twp['Points'], twp['Distance']))
          #n += 1


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
