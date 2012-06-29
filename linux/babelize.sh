#!/bin/sh

. /etc/schwinn810.conf

if command -v gpsbabel &> /dev/null ; then
    gpsbabel -i unicsv,utc=$OFFSET -f "$1.points" \
	-x transform,trk=wpt \
	-o gpx -F "$1.gpx" \
	-o kml,lines=1,points=0,track=1,trackdirection=1 -F "$1.kml"
fi

/usr/share/schwinn810/csv2tcx.py "$1" > "$1.tcx"
