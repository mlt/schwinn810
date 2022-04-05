#!/usr/bin/env python
from __future__ import print_function
from core.device import Device, SerialException
from core.writer_csv import Writer
# from extra.writer_sqlite import SQLiteWriter
from core.writer_csv import WriterCSV
from core.writer_tcx import WriterTCX
from core.progress_text import TextProgress
from datetime import timedelta
import argparse, os, sys
import logging
from tabulate import tabulate
from web.tcx2strava import strava_upload

_log = logging.getLogger(__name__)

def main():
    print("""schwinn810  Copyright (C) 2012 Mikhail Titov

This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under the terms of GPL-3 or later version.
""")

    parser = argparse.ArgumentParser(description='Download tracks from Schwinn 810 GPS sport watch with HRM.')
    parser.add_argument('--port', nargs=1,
                        default=[ {'posix': '/dev/ttyUSB0', 'nt': 'COM5'}[os.name] ],
                        help='Virtual COM port created by cp201x for Schwinn 810 GPS watch')
    parser.add_argument('--hook', nargs=1, default = [ None ],
                        help='Callback upon track extraction')
    parser.add_argument('--dir', nargs=1,
                        default=['.'],
                        help='Where to store data')
    parser.add_argument('--debug', action='store_true',
                        help='Dump all replies in a binary form into a single file schwinn810.bin in TEMP dir')
    parser.add_argument('--delete', action='store_true',
                        help='Delete all data from watches after download?')
    parser.add_argument('--logfile', help='file to which logs should be written')
    parser.add_argument('--progress', choices=['none', 'text', 'gtk', 'qt'],
                        default=['text'],
                        help='Progress indicator')
    parser.add_argument('--read-settings', action='store_true',
                        help='Retrieve settings from watch')
    parser.add_argument('--shift', type=float, help='Time adjustments in hours to apply if wrong TZ was set')
    parser.add_argument('--strava', action='store_true', help='upload written files to strava. (only works with --writer tcx)')
    parser.add_argument('--writer', choices=['tcx', 'csv'],
                        default=['tcx'],
                        help='The output writer to use')
    parser.add_argument('--watch-type', choices=['soleus', 'schwinn', 'cresta'],
                        default=None,
                        help='The type of watch that you are trying to download data from')
    # parser.add_argument('--add-year', dest='add_year', action='store_true',
    #                    help='Creates subfolder in dir named after the current year')
    # parser.add_argument('--add-id', dest='add_id', action='store_true',
    #                    help='Creates subfolder with device id inside dir but before year')

    args = parser.parse_args()

    if args.strava and args.writer != 'tcx':
      print("Error:  You must use the tcx writer if you want to upload to strava")
      sys.exit(1)

    if args.logfile:
      logging.basicConfig(level=logging.DEBUG, filename=args.logfile, filemode='w')
    else:
      logging.basicConfig(level=logging.WARNING)

    try:
        d = Device(device=args.port[0], debug=args.debug, watch_type=args.watch_type)
        # w = SQLiteWriter(args.dir[0], args.hook[0])
        if args.writer == 'tcx':
          w = WriterTCX(args.dir[0], args.hook[0])
        else:
          w = WriterCSV(args.dir[0], args.hook[0])
        p = None
        if args.progress != 'none':
            p = TextProgress()  # default progress
        if args.progress == 'gtk':
            try:
                from core.progress_gtk import GtkProgress
                p = GtkProgress()
            except ImportError:
                _log.error('Failed to create GTK backend')
        elif args.progress == 'qt':
            try:
                from PyQt4.QtGui import QApplication
                from core.progress_qt import QtProgress
                app = QApplication(sys.argv)
                p = QtProgress()
            except ImportError:
                _log.error('Failed to create QT backend')
        if args.shift:
            d.shift = timedelta(hours=args.shift)
            _log.info("Applying {:f} hours shift".format(args.shift))
        d.read(w, p)

        if(len(w.tracks_written()) > 0 ):
          table_rows = []
          n = 1
          for track in w.tracks_written():
            table_rows.append([n, track['Track'], track['Start'], track['End'] - track['Start'], "%.1fkm/h" % (track['Speed']), track['Laps'], track['Points'], "%.2fkm" % (track['Distance'])])
            n += 1
          print(tabulate(table_rows, headers=["Track","Label","Started At","Duration","Speed","Laps","Points","Distance"]))
            
          if args.strava:
            chosentracklist = raw_input("choose tracks to upload (eg. 1,3,4):")
            chosentrackints = [(int(x.strip()) - 1) for x in chosentracklist.split(",")]
            chosentracks = [w.tracks_written()[n]['Filename'] for n in chosentrackints]

            strava_upload(chosentracks)

        
        if args.read_settings:
            _log.info("Reading settings")
            d.read_settings(w)
        if args.delete:
            d.clear()
        d.close()

    except SerialException as e:
        _log.fatal("Port can't be opened :(")
        sys.exit(-1)

    print("Done")

if __name__ == '__main__':
    # FORMAT = FORMAT = '%(asctime)-15s %(message)s'
    # logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    main()
