""" Device class to communicate with Soleus 810 """

from __future__ import print_function
import struct
from utils import *
import logging
from datetime import datetime, time, date
from reader import *
from reader_schwinn import SchwinnReader
import sys
# from binascii import hexlify

_log = logging.getLogger(__name__)

class SoleusReader(SchwinnReader):

    def __init__(self, port, dump=None):
        super(SoleusReader, self).__init__(port, dump)

    def read_summary(self):
        #_log.debug("read summary 0x{:x}".format(self._port.tell()))
        _log.debug("read summary")
        raw = self.read(0x24)
        s = {}
        (s['T1'], s['T2'] , s['24hr'], tracks1, sign1, tracks2, sign2) = \
             struct.unpack("<2B 6x B 19x 4H", raw)
        if(tracks1 != tracks2 or sign1 != sign2 or sign1 != 0xff00):
          raise BadSignature("Unexpected pattern found for Soleus Watch.  Is this a Soleus Watch?")
         
        s['Waypoints'] = 0
        s['Tracks'] = tracks1
        _log.debug("{:d} {:d} {:d} {:d} {:d} {:d}".format(s['T1'], s['T2'] , s['24hr'], s['Tracks'], s['Waypoints'], sign1))
        # a = hexlify(raw)
        # _log.debug(a)
        # return struct.unpack("=28xHH4x", raw)
        return s


if __name__ == '__main__':
    pass
