""" Base reader class for data decoders """

# import logging
# _log = logging.getLogger(__name__)

class NotConnected(Exception): pass
class BadSignature(Exception): pass

class Reader(object):

    def __init__(self, port, dump=None):
        self.port = port
        self.dump = dump

    def read(self, amount):
        raw = self.port.read(amount)
        if self.dump:
            self.dump.write(raw)
        return raw

if __name__ == '__main__':
    pass
