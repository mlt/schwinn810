""" Base reader class for data decoders """

# import logging
# _log = logging.getLogger(__name__)

class NotConnected(Exception): pass
class BadSignature(Exception): pass

class Reader(object):

    def __init__(self, port, dump=None):
        self._port = port
        self._dump = dump

    def read(self, amount):
        raw = self._port.read(amount)
        if self._dump:
            self._dump.write(raw)
        return raw

if __name__ == '__main__':
    pass
