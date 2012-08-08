""" An example demonstrating how to implement custom storage backend for Schwinn 810

SQLite example
"""

import sys,os
import subprocess
import sqlite3
import logging
from collections import deque

_log = logging.getLogger(__name__)

class SQLiteWriter:
    """ SQLite writer """

    track_keys = { 'Start': ('start', 'date'),
                   'End': ('end', 'date'),
                   'Laps': ('laps', 'int'),
                   'MaxHeart': ('heart_max', 'int'),
                   'Heart': ('heart', 'int'),
                   'MaxSpeed': ('speed_max', 'real'),
                   'Speed': ('speed', 'real'),
                   'Points': ('points', 'int'),
                   'Track': ('track', 'text') }

    lap_keys = { 'Time': ('time', 'date'),
                 'Speed': ('speed', 'real'),
                 'Lap': ('lap', 'int'),
                 'Distance': ('distance', 'real'),
                 'kcal': ('kcal', 'real'),
                 'MaxSpeed': ('speed_max', 'real'),
                 'autolap': ('autolap', 'int'),
                 'Beats': ('beats', 'int'),
                 'sec': ('sec', 'int'),
                 'MaxHeart': ('heart_max', 'int'),
                 'MinHeart': ('heart_min', 'int'),
                 'InZone': ('in_zone', 'int'), 
                 'Elevation': ('elevation', 'real') }

    point_keys = { 'Distance': ('distance', 'real'),
                   'Speed': ('speed', 'real'),
                   'Time': ('time', 'date'),
                   'Heart': ('heart', 'real'),
                   # 'InZone': ('in_zone', 'int'),
                   'Latitude': ('lat', 'real'),
                   'Longitude': ('lon', 'real'),
                   'kcal': ('kcal', 'real'),
                   'Elevation': ('elevation', 'real')
                   }

    waypoint_keys = { 'Timestamp': ('time', 'date'),
                      'Name': ('name', 'text'),
                      'Latitude': ('lat', 'real'),
                      'Longitude': ('lon', 'real'),
                      'Elevation': ('elevation', 'real')
                      }

    def __init__(self, dir, hook=None):
        self.con = sqlite3.connect(dir)
        self.c = self.con.cursor()
        self.hook = hook

        self.c.execute(self._make_table_sql('tracks', self.track_keys))
        self.c.execute(self._make_table_sql('laps', self.lap_keys))
        self.c.execute(self._make_table_sql('points', self.point_keys))
        self.c.execute(self._make_table_sql('waypoints', self.waypoint_keys))

        self.tracks_with_points = deque()

    @staticmethod
    def _make_table_sql(table, keys):
        sql = "CREATE TABLE IF NOT EXISTS {:s} ({:s}, track_id int)".format(
            table,
            ",".join( [ " ".join(x) for x in keys.itervalues() ] ))
        return sql

    def add_track(self, track):
        """ Append track to database """
        # select only those we want to keep
        fields = [f for f in track.iterkeys() if f in self.track_keys]
        db_fields = [self.track_keys[f][0] for f in fields]
        sql = """INSERT INTO tracks ({:s}) VALUES ({:s})""".format(
            ",".join(db_fields),
            ",".join(['?'] * len(db_fields)) )
        values = [v for i, v in track.iteritems() if i in fields]
        self.c.execute(sql, values)
        self.track = self.c.lastrowid
        if track['Points'] > 0:
            self.tracks_with_points.append(self.track)

    def add_lap(self, lap):
        """ Append lap to a database """
        # select only those we want to keep
        fields = [f for f in lap.iterkeys() if f in self.lap_keys]
        db_fields = [self.lap_keys[f][0] for f in fields]
        sql = """INSERT INTO laps ({:s}, track_id) VALUES ({:s}, ?)""".format(
            ",".join(db_fields),
            ",".join(['?'] * len(db_fields)) )
        values = [v for i, v in lap.iteritems() if i in fields]
        self.c.execute(sql, values + [self.track])

    def begin_points(self, summary):
        """ Points for track will follow """
        self.con.commit()
        self.track = self.tracks_with_points.popleft()

    def add_point(self, point):
        """ Append point to a database """
        # select only those we want to keep
        fields = [f for f in point.iterkeys() if f in self.point_keys]
        db_fields = [self.point_keys[f][0] for f in fields]
        sql = """INSERT INTO points ({:s}, track_id) VALUES ({:s}, ?)""".format(
            ",".join(db_fields),
            ",".join(['?'] * len(db_fields)) )
        values = [v for i, v in point.iteritems() if i in fields]
        self.c.execute(sql, values + [self.track])

    def commit(self):
        """ Commit last track in a database """
        self.con.commit()

    def add_waypoint(self, wp):
        """ Append point to a database """
        # select only those we want to keep
        fields = [f for f in wp.iterkeys() if f in self.wp_keys]
        db_fields = [self.wp_keys[f][0] for f in fields]
        sql = """INSERT INTO waypoints ({:s}) VALUES ({:s})""".format(
            ",".join(db_fields),
            ",".join(['?'] * len(db_fields)) )
        values = [v for i, v in wp.iteritems() if i in fields]
        self.c.execute(sql, values)
        self.con.commit()

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    w = SQLiteWriter("/home/mlt/schwinn810.db")
