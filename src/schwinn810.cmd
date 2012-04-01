@echo off

rem start
download.exe ^
 --port schwinn810.bin ^
 --hook %~dp0\babelize.cmd ^
 --dir "%HOME%\Documents\My Runs"
rem  --port COM6 ^

SET "GPSBABEL=C:\Program Files\GPSBabel\gpsbabel.exe"
SET "Z7=C:\Program Files\7-Zip\7z.exe"

"%GPSBABEL%" -i unicsv,utc=5 -f "%HOME%\Documents\My Runs\waypoints.csv" ^
 -o gpx -F "%HOME%\Documents\My Runs\waypoints.gpx" ^
 -o kml,lines=1,points=0,track=1,trackdirection=1 -F "%HOME%\Documents\My Runs\waypoints.kml"

%COMSPEC% /C DEL /Q /F "%HOME%\Documents\My Runs\waypoints.kmz" > nul

"%Z7%" a -tzip "%HOME%\Documents\My Runs\waypoints.kmz" "%HOME%\Documents\My Runs\waypoints.kml" > nul
