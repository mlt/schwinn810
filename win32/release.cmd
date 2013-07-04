@echo off

set VER=0.2rc2

rd /S /Q build

pushd ..\src
C:\OSGeo4W\bin\python setup-win32.py build -b ..\win32\build
popd

7z a -xr!*.py* build\exe.win32-2.7\library.zip C:\OSGeo4W\apps\python27\lib\site-packages\pytz > nul

copy *_sample.cmd build\exe.win32-2.7\

pushd build
ren exe.win32-2.7 schwinn810_%VER%_win32
7z a -r schwinn810_%VER%_win32.zip schwinn810_%VER%_win32
popd
