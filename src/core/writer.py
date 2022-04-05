""" Simple CSV writer for Schwinn 810 """

import sys,os
import subprocess
import csv
import logging

_log = logging.getLogger(__name__)

open_extra = {}
if sys.version_info >= (3,0):
    open_extra["newline"] = ''

class Writer:
    """ Default files writer """

    def __init__(self, dir, hook=None):
      """ this should be implemented """
      raise NotImplementedError( "Should have implemented this" )
  
    def add_track(self, track):
      """ this should be implemented """
      raise NotImplementedError( "Should have implemented this" )
  
    def add_waypoint(self, track):
      """ this should be implemented, but not sure what it does """
      raise NotImplementedError( "Should have implemented this" )

    def tracks_written(self):
      return []
      

if __name__ == '__main__':
    pass
