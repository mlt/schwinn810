""" Device class to communicate with Schwinn 810 """

from __future__ import print_function
import struct
from utils import *
import logging
from datetime import datetime, time, date
from reader import *
import sys
# from binascii import hexlify

_log = logging.getLogger(__name__)

class SchwinnReader(Reader):

    def __init__(self, port, dump=None):
        super(SchwinnReader, self).__init__(port, dump)

    def read_summary(self):
        #_log.debug("read summary 0x{:x}".format(self._port.tell()))
        _log.debug("read summary")
        raw = self.read(0x24)
        s = {}
        (s['T1'], s['T2'] , s['24hr'], s['Tracks'], s['Waypoints'], sign) = \
             struct.unpack("<2B 6x B 19x 2H 3x B", raw)
        _log.debug("{:d} {:d} {:d} {:d} {:d} {:d}".format(s['T1'], s['T2'] , s['24hr'], s['Tracks'], s['Waypoints'], sign))
        # a = hexlify(raw)
        # _log.debug(a)
        # return struct.unpack("=28xHH4x", raw)
        return s

    def read_track(self):
        _log.debug("read track header 0x{:x}".format(self.bytes_read))
        raw = self.read(0x24)
        track = {}
        (sec1,min1, hr1, dd1, mm1, yr1, lap_count, \
             speed_max, speed, track['MaxHeart'], track['x4'], track['Points'], \
             track['x5'], name0, track['Heart'], min2, hr2, dd2, mm2, yr2, sign) = \
             struct.unpack(">6BH HHBBH H7sB5B4xB", raw)
        _log.debug("0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} {:s} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x}".format(sec1,min1, hr1, dd1, mm1, yr1, lap_count, speed_max, speed, track['MaxHeart'], track['x4'], track['Points'], track['x5'], name0, track['Heart'], min2, hr2, dd2, mm2, yr2, sign))
        rawbytes = struct.unpack("36B", raw)
        _log.debug(" ".join(["0x%x" % x for x in rawbytes]))
        if 0xFD != sign:
            raise BadSignature
        track['End'] = datetime(2000+yr2, mm2, dd2, hr2, min2)
        track['Start'] = datetime(2000+yr1, mm1, dd1, hr1, min1, sec1)
        track['Laps'] = lap_count - 1
        track['Speed'] = speed/10.
        track['MaxSpeed'] = speed_max/10.
        track['Track'] = name0.decode('ascii')
        #track['Distance'] = ((track['Speed']) * ((track['End']-track['Start']).total_seconds())) / 3600.0
        return track

    def read_lap(self):
        raw = self.read(0x24)
        lap = {}
        (hh, mm, ss, sss, dist, \
             cal, speed_max, speed, \
             lap['autolap'], beats_high, beats_mid, beats_low, lap['sec'], lap['MaxHeart'], lap['MinHeart'], \
             iz_h, iz_m, iz_s, lap['y4'], z0, \
             lap['Lap'], track_number, sign) = \
            struct.unpack(">4BI IxBxB 4BH2B 3BB4s HBB", raw)
        _log.debug("read lap header")
        _log.debug("0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} {:s} 0x{:x} 0x{:x} 0x{:x}".format(hh, mm, ss, sss, dist, \
             cal, speed_max, speed, \
             lap['autolap'], beats_high, beats_mid, beats_low, lap['sec'], lap['MaxHeart'], lap['MinHeart'], \
             iz_h, iz_m, iz_s, lap['y4'], z0, \
             lap['Lap'], track_number, sign))
        #rawbytes = struct.unpack("36B", raw)
        #_log.debug(" ".join(["0x%x" % x for x in rawbytes]))
        if 0xFD != sign:
            raise BadSignature()
        lap['InZone'] = iz_h*3600 + iz_m*60 + iz_s
        lap['Elevation'] = struct.unpack("<I", z0)[0]/1e2
        lap['HasElevation'] = (lap['Elevation'] != 0.0)
        lap['Time'] = hh*3600 + mm*60 + ss + sss/100.
        lap['Speed'] = speed/10.
        lap['Distance'] = dist/1e5
        lap['kcal'] = cal/1e4
        lap['MaxSpeed'] = speed_max/10.
        lap['Beats'] = beats_high << 16 | beats_mid << 8 | beats_low
        return lap

    def read_points_summary(self):
        _log.debug("read points summary 0x{:x}".format(self.bytes_read))
        raw = self.read(0x24)
        _log.debug("read points summary " + str(len(raw)))
        (sec1, min1, hr1, dd1, mm1, yr1, lap_count, hrm, pts, name0, ahr, min2, hr2, dd2, mm2, yr2, sign) = \
            struct.unpack(">6BH4xBxHxx7sB5B4xB", raw)
        _log.debug("0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} {:s} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x}".format(sec1, min1, hr1, dd1, mm1, yr1, lap_count, hrm, pts, name0, ahr, min2, hr2, dd2, mm2, yr2, sign))
        if 0xFA != sign:
            raise BadSignature
        track_name = name0.decode('ascii')
        return {'Track': track_name, 'Points': pts, 'Start': datetime(2000+yr1, mm1, dd1, hr1, min1, sec1)}

    def read_point(self):
        #_log.debug("read point")
        raw = self.read(0x24)
        point = {}
        (dist0, speed, sec, min, hr, x1, hrm, izhh, izss, izmm, lat0, lon0, \
             raw2, pt, trk, sign) = \
             struct.unpack(">4sH3BBH3B5s6s 6sHBB", raw)
        #_log.debug("0x{:s} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:x} 0x{:s} 0x{:s} 0x{:s} 0x{:x} 0x{:x} 0x{:x}".format(dist0, speed, sec, min, hr, x1, hrm, izhh, izss, izmm, lat0, lon0, raw2, pt, trk, sign))
        #_log.debug(" ".join(["0x%x" % x for x in struct.unpack("36B", raw)]))
        if 0xFA != sign:
            raise BadSignature
        (cal, z) = struct.unpack("<HI", raw2)
        point['kcal'] = cal
        point['Elevation'] = z / 1e2
        point['Distance'] = struct.unpack("<I", dist0)[0] / 1e5
        point['Speed'] =speed/160.9 # really?
        point['Heart'] = hrm/5
        point['No'] = pt
        point['Time'] = time(hr, min, sec)
        # time = "20{:02d}-{:d}-{:d} {:02d}:{:02d}:{:02d}".format(yr1, mm1, dd1, hr, min, sec)
        point['Latitude'] = pack_coord(b"\x00" + lat0, b'S')
        point['Longitude'] = pack_coord(lon0, b'W')
        point['InZone'] = izhh*3600 + izmm*60 + izss
        return point

    def read_waypoint(self):
        raw = self.read(0x24)
        byte_a = bytearray(raw)
        
        for i in byte_a:
          sys.stdout.write(format(i, '02x') + " ")
        wpt = {}
        (yy, mm, dd, hh, mn, ss, name0, lat0, lon0, x1,x2, z, num, sign) = \
            struct.unpack("=6B6s3x5s6s2BH4xBB", raw)
        wpt['Time'] = datetime(2000+yy, mm, dd, hh, mn, ss)
        wpt['Name'] = name0.decode('ascii')
        wpt['Latitude'] = pack_coord(b"\x00" + lat0, b'S')
        wpt['Longitude'] = pack_coord(lon0, b'W')
        wpt['Elevation'] = z/1e2
        return wpt

    def read_end(self):
        raw = self.read(0x24)
        # a = hexlify(raw)
        # _log.debug(a)

    def read_settings(self):
        """ Autolap: off, 0.4, 1, 2, 3, 4, 5 """
        raw = self.read(0x25)
        # a = hexlify(raw)
        # _log.debug(a)
        s = {}
        (s['Female'], s['Age'], s['Metric'], s['x3'],  s['kg'], s['cm'], s['zone_active'], \
             s['zone1_low'],  s['zone1_high'], s['zone2_low'], s['zone2_high'], s['zone3_low'],\
             s['zone3_high'], s['zone_alarm'], s['x5'], s['Autolap'], s['Contrast'], s['x8'], s['NightMode'], \
             s['y2'], s['lb'], s['in'], s['24hr'], s['y6'], s['y7'], s['y8'], s['z1'], s['z2'], sign1, sign2) = \
             struct.unpack("=28B2I", raw)
        # contrast 8 => 50%
        # x5=alert
        # raw = self.read(0x24)
        # a = hexlify(raw)
        # _log.debug(a)
        # _log.debug(s)
        return s

if __name__ == '__main__':
    pass
