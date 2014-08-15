@echo off

SET "DIR=%USERPROFILE%\Documents\My Runs"
SET "GPSBABEL=C:\Programs\GPSBabel\gpsbabel.exe"
SET "Z7=C:\Program Files\7-Zip\7z.exe"

%~dp0\download.exe ^
 --hook %~dp0babelize.cmd ^
 --progress qt ^
 --delete ^
 --debug ^
 --dir "%DIR%"

"%GPSBABEL%" -i unicsv,utc=5 -f "%DIR%\waypoints.csv" ^
 -o gpx -F "%DIR%\waypoints.gpx" ^
 -o kml,lines=1,points=0,track=1,trackdirection=1 -F "%DIR%\waypoints.kml"

rem %COMSPEC% /C DEL /Q /F "%DIR%\waypoints.kmz" > nul

rem "%Z7%" a -tzip "%DIR%\waypoints.kmz" "%DIR%\waypoints.kml" > nul
