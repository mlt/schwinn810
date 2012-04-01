@echo off
SET "GPSBABEL=C:\Program Files\GPSBabel\gpsbabel.exe"
SET "Z7=C:\Program Files\7-Zip\7z.exe"

"%GPSBABEL%" -i unicsv,utc=5 -f %1.points ^
 -o gpx -F %1.gpx ^
 -o gtrnctr,sport=Running,course=0 -x transform,trk=wpt,del -F %1.tcx ^
 -o kml,lines=1,points=0,track=1,trackdirection=1 -F %1.kml

%COMSPEC% /C DEL /Q /F %1.kmz

"%Z7%" a -tzip %1.kmz %1.kml > nul
