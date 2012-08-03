#!/bin/sh

. /etc/schwinn810/schwinn810.conf

# Get KML & GPX if we have gpsbabel installed
if command -v gpsbabel &> /dev/null ; then
    gpsbabel -i unicsv,utc=$OFFSET -f "$1.points" \
	-x transform,trk=wpt,del \
	-o gpx -F "$1.gpx" \
	-o kml,lines=1,points=0,track=1,trackdirection=1 -F "$1.kml"
fi

/usr/share/schwinn810/csv2tcx.py "$1" > "$1.tcx"

# Upload TCX to web. See source code for details
# /usr/share/schwinn810/web/tcx2web.py "%1.tcx"
