#!/usr/bin/env python
# Use https://github.com/chmouel/python-garmin-upload
# Don't forget patch https://github.com/chmouel/python-garmin-upload/issues/1
# Create ~/.schwinn810.yaml with the following 3 lines
# garmin:
#   username: your_garmin_connect_user_name
#   password: your_password

import argparse
#from UploadGarmin import UploadGarmin
from antd import connect        # requires python-poster
from yaml import load, dump
import os, logging

logging.basicConfig()

parser = argparse.ArgumentParser(description='Uploads TCX to Garmin Connect')
parser.add_argument(nargs='+', dest='tcx', help='TCX files to upload')
args = parser.parse_args()

stream = file(os.path.expanduser('~/.schwinn810.yaml'), 'r')
cfg = load(stream)
cfg = cfg['garmin']

client = connect.GarminConnect()
client.username = cfg["username"]
client.password = cfg["password"]

client.data_available(None, "tcx", args.tcx)
#client.upload("tcx", name)

# g = UploadGarmin()

# print("Using %s and %s to connect" % (cfg["username"], cfg["password"]))
# g.login(cfg["username"], cfg["password"])

# print("Uploading %s" % args.tcx)
# wId = g.upload_ctx(args.tcx)

# print("Renaming it to %s" % name[0])
# g.name_workout(wId, name[0])

