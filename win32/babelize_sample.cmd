@echo off
SET "GPSBABEL=C:\Program Files\GPSBabel\gpsbabel.exe"
SET "Z7=C:\Program Files\7-Zip\7z.exe"

REM Convert points into GPX and KML
REM See manual for GPSBabel for options
REM For TCX conversion see below
"%GPSBABEL%" -i unicsv,utc=5 -f "%1.points" ^
 -x transform,trk=wpt,del ^
 -o gpx -F "%1.gpx" ^
 -o kml,lines=1,points=0,track=1,trackdirection=1 -F "%1.kml"

rem -o gtrnctr,sport=Running,course=0 -F %1.tcx ^

%~dp0\csv2tcx.exe "%1" > "%1.tcx"

REM Make a compressed Google Earth file
REM %COMSPEC% /C DEL /Q /F "%1.kmz"
REM "%Z7%" a -tzip "%1.kmz" "%1.kml" > nul

REM Upload TCX to web. See source code for details
REM %~dp0\tcx2web.exe "%1.tcx"
