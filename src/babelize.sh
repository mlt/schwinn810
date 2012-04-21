#!/bin/sh

gpsbabel -i unicsv,utc=5 -f "$1.points" \
	-x transform,trk=wpt \
	-o gpx -F "$1.gpx" \
	-o kml,lines=1,points=0,track=1,trackdirection=1 -F "$1.kml"

DIR="$(dirname "${BASH_SOURCE[0]}")"
/usr/bin/python "$DIR/csv2tcx.py" "$1" > "$1.tcx"
NAME=$(basename "$1")
#perl "$DIR/../mapmyrun/mmr_uploader.pl" $NAME "$1.tcx"

