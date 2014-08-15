@echo off
setlocal

set NAME=%~1

echo Postprocessing "%NAME%"
cd /d "%~dp0"

SET "GPSBABEL=C:\OSGeo4W64\bin\gpsbabel.exe"
SET "Z7=C:\Program Files\7-Zip\7z.exe"
rem SET "Z7=C:\Program Files (x86)\7-Zip\7z.exe"

REM Convert points into GPX and KML
REM See manual for GPSBabel for options
REM For TCX conversion see below
"%GPSBABEL%" -i unicsv,utc=5 -f "%NAME%.points" ^
 -x transform,trk=wpt,del ^
 -o gpx -F "%NAME%.gpx" ^
 -o kml,lines=1,points=0,track=1,trackdirection=1 -F "%NAME%.kml"

rem Compress KML into KMZ
DEL /Q /F "%NAME%.kmz" 2> nul
"%Z7%" a -tzip "%NAME%.kmz" "%NAME%.kml" > nul

rem Get TCX
csv2tcx.exe "%NAME%" > "%NAME%.tcx"

REM Make a compressed Google Earth file
REM %COMSPEC% /C DEL /Q /F "%1.kmz"
REM "%Z7%" a -tzip "%1.kmz" "%1.kml" > nul

set REQUESTS_CA_BUNDLE=%~dp0cacert.pem
REM Upload TCX to web. See source code for details
%~dp0\tcx2web.exe "%NAME%.tcx"

endlocal
