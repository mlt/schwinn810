@echo off
setlocal

set VER=0.3

set OSGEO4W_ROOT=C:\OSGeo4W64
set PYTHON=%OSGEO4W_ROOT%\bin\python.exe
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27

set CPU=x86
set EXT=win32

for /f "usebackq" %%i in (`%PYTHON% -c "import sys;print(sys.maxsize>2**32)"`) do set IS64=%%i

if "%IS64%" == "True" (
  set CPU=x64
  set EXT=win-amd64
)

rd /S /Q build

pushd ..
%OSGEO4W_ROOT%\bin\python setup-win32.py build -b win32\build
popd

rem pytz now is in egg, unpack relevant files into local pytz subfolder
7za a -xr!*.py* build\exe.%EXT%-2.7\library.zip pytz > nul
rem 7za a -xr!*.py* build\exe.%EXT%-2.7\library.zip %OSGEO4W_ROOT%\apps\python27\lib\site-packages\pytz > nul

copy *_sample.cmd build\exe.%EXT%-2.7\
copy ..\schwinn810\%CPU%\SiUSBXp.dll build\exe.%EXT%-2.7\

pushd build
ren exe.%EXT%-2.7 schwinn810_%VER%_%EXT%
7za a -r schwinn810_%VER%_%EXT%.zip schwinn810_%VER%_%EXT% > nul
popd

endlocal
