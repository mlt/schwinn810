@echo off

set OSGEO4W_ROOT=C:\OSGeo4W64
set PYTHON=%OSGEO4W_ROOT%\bin\python.exe
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27

set NAME=%~1

echo Postprocessing "%NAME%"
cd /d "%~dp0"

SET "GPSBABEL=C:\OSGeo4W64\bin\gpsbabel.exe"
rem SET "GPSBABEL=C:\Program Files\GPSBabel\gpsbabel.exe"
SET "Z7=C:\Program Files (x86)\7-Zip\7z.exe"

rem Get GPX & KML
"%GPSBABEL%" -i unicsv,utc=5 -f "%NAME%.points" ^
 -x transform,trk=wpt,del ^
 -o gpx -F "%NAME%.gpx" ^
 -o kml,lines=1,points=0,track=1,trackdirection=1 -F "%NAME%.kml"

rem Compress KML into KMZ
DEL /Q /F "%NAME%.kmz" 2> nul
"%Z7%" a -tzip "%NAME%.kmz" "%NAME%.kml" > nul

rem Get TCX
%PYTHON% csv2tcx.py "%NAME%" > "%NAME%.tcx"

rem Upload TCX to web. See source code for details
rem web\tcx2web.exe "%1.tcx"
