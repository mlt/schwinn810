#!/usr/bin/python

import sys

from setuptools import setup, find_packages

setup( name = "schwinn810",
       version = "0.3",
       license='GPL-3',
       description = "Tools for Schwinn 810 GPS sport watch",
       author = "Mikhail Titov",
       author_email = "mlt@gmx.us",
       url = "https://github.com/mlt/schwinn810",
       download_url = 'https://github.com/mlt/schwinn810/archive/master.zip',
       install_requires = [
           'pyserial',
           'appdirs',
           'pytz',
           'requests'
       ],
       classifiers = [
           'Development Status :: 4 - Beta',
           'Environment :: Console',
           'Environment :: Win32 (MS Windows)',
           'Environment :: X11 Applications',
           'Intended Audience :: End Users/Desktop',
           'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
           'Operating System :: OS Independent',
           'Programming Language :: Python'
       ],
       packages = find_packages(),
       data_files = [("share/schwinn810", ["linux/babelize.sh"] )],
       package_data = { "schwinn810": ["progress.glade"] },
       include_package_data=True,
       entry_points = {
           'console_scripts': [
               'schwinn810 = schwinn810.download:main'
           ],
           'gui_scripts': [
           'schwinn810-tray = schwinn810.tray_gtk:main'
           ]
       },
       test_suite = "schwinn810.tests")
