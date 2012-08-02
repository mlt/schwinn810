#!/usr/bin/env python
from __future__ import print_function
from core.device import Device, SerialException
from core.writer_csv import Writer
from core.progress_text import TextProgress
import argparse, os
import logging

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
    parser.add_argument('--progress', choices=['text', 'gtk'],
                        default=['text'],
                        help='Progress indicator')
    # parser.add_argument('--add-year', dest='add_year', action='store_true',
    #                    help='Creates subfolder in dir named after the current year')
    # parser.add_argument('--add-id', dest='add_id', action='store_true',
    #                    help='Creates subfolder with device id inside dir but before year')

    args = parser.parse_args()

    d = Device(args.port[0])
    d.debug = args.debug
    try:
        w = Writer(args.dir[0], args.hook[0])
        p = TextProgress()
        if args.progress == 'gtk':
            try:
                from core.progress_gtk import GtkProgress
                p = GtkProgress()
            except ImportError:
                _log.error('Failed to create GTK backend')
        d.read(w, p)
        d.close()
    except SerialException as e:
        _log.fatal("Port can't be opened :(")
        exit(-1)

    print("Done")

if __name__ == '__main__':
    # FORMAT = FORMAT = '%(asctime)-15s %(message)s'
    # logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logging.basicConfig(level=logging.WARNING)
    main()
