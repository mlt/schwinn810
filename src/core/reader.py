""" Base reader class for data decoders """

import logging
_log = logging.getLogger(__name__)

class NotConnected(Exception): pass
class BadSignature(Exception): pass
class UnknownWatchType(Exception): pass
class BadRead(Exception): pass

class Reader(object):

    def __init__(self, port, dump=None):
        self._port = port
        self._dump = dump
        self.bytes_read = 0

    def read(self, amount):
        raw = "" 
        n = 0
        while(amount != len(raw)):
          if(n > 0): 
            _log.debug("only read %s of %s bytes on the last pass. %s left to read " % (len(tmp), amount,  amount - len(raw)))
          tmp = self._port.read(amount - len(raw))
          self.bytes_read = len(tmp) + self.bytes_read
          if self._dump:
            self._dump.write(tmp)
          if(len(tmp) == 0):
            raise BadRead("no bytes received from port while try to read after %s bytes read" % self.bytes_read)
          raw += tmp
          n += 1

        return raw

    def current_read_offset():
        return self.bytes_read

if __name__ == '__main__':
    pass
