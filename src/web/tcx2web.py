#!/usr/bin/env python
# Create ~/.schwinn810.yaml with the following 3 lines
# garmin:
#   username: your_garmin_connect_user_name
#   password: your_password
# mmf:
#   username: your_mmf_user_name
#   password: your_password

import argparse
from antd import connect        # requires python-poster
from mmf import MMF
from yaml import load, dump
import os, logging
import thread

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Uploads TCX to the Internets')
    parser.add_argument(nargs='+', dest='tcx', help='TCX files to upload')
    args = parser.parse_args()

    stream = file(os.path.expanduser('~/.schwinn810.yaml'), 'r')
    cfg = load(stream)

    if 'garmin' in cfg:
        garmin = cfg['garmin']

        client = connect.GarminConnect()
        client.username = cfg["username"]
        client.password = cfg["password"]

        client.data_available(None, "tcx", args.tcx)
        # thread.start_new_thread()

    if 'mmf' in cfg:
        mmv = cfg['mmf']

        client = MMF()
        client.username = mmf["username"]
        client.password = mmf["password"]

        client.data_available(None, "tcx", args.tcx)

    # join

if __name__ =='__main__':
    main()
