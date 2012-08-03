@echo off
cd /d "%~dp0"

SET "GPSBABEL=C:\Program Files\GPSBabel\gpsbabel.exe"
SET "Z7=C:\Program Files\7-Zip\7z.exe"

rem Get GPX & KML
"%GPSBABEL%" -i unicsv,utc=5 -f "%1.points" ^
 -x transform,trk=wpt,del ^
 -o gpx -F "%1.gpx" ^
 -o kml,lines=1,points=0,track=1,trackdirection=1 -F "%1.kml"

rem Compress KML into KMZ
DEL /Q /F "%1.kmz"
"%Z7%" a -tzip "%1.kmz" "%1.kml" > nul

rem Get TCX
csv2tcx.exe "%1" > "%1.tcx"

rem Upload TCX to web. See source code for details
rem web\tcx2web.exe "%1.tcx"
