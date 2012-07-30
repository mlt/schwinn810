""" Simple text based progress indicator """

from __future__ import print_function

class TextProgress:

    def track(self, at, end):
        print("Fetching track {:d}/{:d}".format(at, end))

    def point(self, at, end):
        if at % 100 == 0:
            print("{:.0f}%".format(100.*at/end))
