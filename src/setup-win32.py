import sys
from cx_Freeze import setup, Executable

# C:\Python27\python setup.py build
# 7z a -xr!*.py* build\exe.win32-2.7\library.zip C:\Python27\Lib\site-packages\pytz

sys.path.append('web')

# Dependencies are automatically detected, but it might need fine tuning.
#"build_exe": "schwinn810_win32",
#  "include-in-shared-zip": ["C:\\Python27\\lib\\site-packages\\pytz\\zoneinfo", "site-packages\\pytz\\zoneinfo"], \
#	"zip_includes": [("C:/Python27/Lib/site-packages/pytz/zoneinfo/", "pytz/zoneinfo/")], \
build_exe_options = {"packages": ["serial.win32"],  \
                         "optimize": 2} #, "create-shared-zip": True}
#"path": [sys.path, "garmin"], "includes": ["UploadGarmin"],

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(  name = "schwinn810",
        version = "0.1",
        description = "Tools for Schwinn 810 GPS sport watch",
        options = {"build_exe": build_exe_options},
        data_files = [(".", ["schwinn810.cmd", "babelize.cmd"] )],
        executables = [Executable("download.py", base=base), \
                           Executable("settings.py", base=base), \
                           Executable("csv2tcx.py", base=base), \
                           Executable("web/tcx2web.py", base=base)])
