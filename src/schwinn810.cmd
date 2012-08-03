@echo off
cd /d "%~dp0"

SET "DIR=%USERPROFILE%\Documents\My Runs"

download.exe ^
 --port COM1 ^
 --hook %~dp0\babelize.cmd ^
 --dir "%DIR%"

SET "GPSBABEL=C:\Program Files\GPSBabel\gpsbabel.exe"
SET "Z7=C:\Program Files\7-Zip\7z.exe"

"%GPSBABEL%" -i unicsv,utc=5 -f "%DIR%\waypoints.csv" ^
 -o gpx -F "%DIR%\waypoints.gpx" ^
 -o kml,lines=1,points=0,track=1,trackdirection=1 -F "%DIR%\waypoints.kml"

%COMSPEC% /C DEL /Q /F "%DIR%\waypoints.kmz" > nul

"%Z7%" a -tzip "%DIR%\waypoints.kmz" "%DIR%\waypoints.kml" > nul
