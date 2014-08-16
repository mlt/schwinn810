@echo off
setlocal

set CPU=x64
set OSGEO4W_ROOT=C:\OSGeo4W64
set PYTHON=%OSGEO4W_ROOT%\bin\python.exe
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27

set VER=0.2rc2

rd /S /Q build

rem set EXT=win32
set EXT=win-amd64

pushd ..\src
%OSGEO4W_ROOT%\bin\python setup-win32.py build -b ..\win32\build
popd

rem pytz now is in egg, unpack relevant files into local pytz subfolder
7za a -xr!*.py* build\exe.%EXT%-2.7\library.zip pytz > nul
rem 7za a -xr!*.py* build\exe.%EXT%-2.7\library.zip %OSGEO4W_ROOT%\apps\python27\lib\site-packages\pytz > nul

copy *_sample.cmd build\exe.%EXT%-2.7\
copy %CPU%\SiUSBXp.dll build\exe.%EXT%-2.7\

pushd build
ren exe.%EXT%-2.7 schwinn810_%VER%_%EXT%
7za a -r schwinn810_%VER%_%EXT%.zip schwinn810_%VER%_%EXT% > nul
popd

endlocal
