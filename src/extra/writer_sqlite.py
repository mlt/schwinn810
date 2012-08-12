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

    track_keys = { 'Start': ('start', 'date unique'),
                   'End': ('end', 'date'),
                   'Laps': ('laps', 'integer'),
                   'MaxHeart': ('heart_max', 'integer'),
                   'Heart': ('heart', 'integer'),
                   'MaxSpeed': ('speed_max', 'real'),
                   'Speed': ('speed', 'real'),
                   'Points': ('points', 'integer'),
                   'Track': ('track', 'text'),
                   '__foo': ('track_id', 'integer primary key autoincrement')}

    lap_keys = { 'Time': ('time', 'date'),
                 'Speed': ('speed', 'real'),
                 'Lap': ('lap', 'integer'),
                 'Distance': ('distance', 'real'),
                 'kcal': ('kcal', 'real'),
                 'MaxSpeed': ('speed_max', 'real'),
                 'autolap': ('autolap', 'integer'),
                 'Beats': ('beats', 'integer'),
                 'sec': ('sec', 'integer'),
                 'MaxHeart': ('heart_max', 'integer'),
                 'MinHeart': ('heart_min', 'integer'),
                 'InZone': ('in_zone', 'integer'), 
                 'Elevation': ('elevation', 'real') }

    point_keys = { 'Distance': ('distance', 'real'),
                   'Speed': ('speed', 'real'),
                   'Time': ('time', 'date primary key'),
                   'Heart': ('heart', 'real'),
                   # 'InZone': ('in_zone', 'integer'),
                   'Latitude': ('lat', 'real'),
                   'Longitude': ('lon', 'real'),
                   'kcal': ('kcal', 'real'),
                   'Elevation': ('elevation', 'real')
                   }

    waypoint_keys = { 'Time': ('time', 'date primary key'),
                      'Name': ('name', 'text'),
                      'Latitude': ('lat', 'real'),
                      'Longitude': ('lon', 'real'),
                      'Elevation': ('elevation', 'real')
                      }

    def __init__(self, dir, hook=None):
        self.con = sqlite3.connect(dir)
        self.c = self.con.cursor()
        self.hook = hook

        self.c.execute('PRAGMA foreign_keys = ON')
        self.c.execute(self._make_table_sql('tracks', self.track_keys))
        self.c.execute(self._make_table_sql(
                'laps', self.lap_keys,
                ", track_id int references tracks(track_id) ON DELETE CASCADE"))
        self.c.execute(self._make_table_sql(
                'points', self.point_keys,
                ", track_id int references tracks(track_id) ON DELETE CASCADE"))
        self.c.execute(self._make_table_sql('waypoints', self.waypoint_keys))

        self.tracks_with_points = deque()

    @staticmethod
    def _make_table_sql(table, keys, extra=None):
        sql = "CREATE TABLE IF NOT EXISTS {:s} ({:s}{:s})".format(
            table,
            ",".join( [ " ".join(x) for x in keys.itervalues() ] ),
            extra if extra else ""
            )
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
        self.track = None
        self.skip = False
        try:
            self.c.execute(sql, values)
            self.c.execute("SELECT track_id FROM tracks WHERE rowid=?", (self.c.lastrowid,))
            self.track = self.c.fetchone()[0]
        except sqlite3.IntegrityError:
            self.skip = True
            _log.info("Already imported. Skipping this track data.")
        if track['Points'] > 0:
            self.tracks_with_points.append((self.track, self.skip))

    def add_lap(self, lap):
        """ Append lap to a database """
        if self.skip:
            return
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
        (self.track, self.skip) = self.tracks_with_points.popleft()

    def add_point(self, point):
        """ Append point to a database """
        if self.skip:
            return
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
        fields = [f for f in wp.iterkeys() if f in self.waypoint_keys]
        db_fields = [self.waypoint_keys[f][0] for f in fields]
        sql = """INSERT INTO waypoints ({:s}) VALUES ({:s})""".format(
            ",".join(db_fields),
            ",".join(['?'] * len(db_fields)) )
        values = [v for i, v in wp.iteritems() if i in fields]
        try:
            self.c.execute(sql, values)
            self.con.commit()
        except sqlite3.IntegrityError:
            pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    w = SQLiteWriter("/home/mlt/schwinn810.db")
