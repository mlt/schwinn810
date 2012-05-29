# About #

There are [inexpensive sport watches](https://www.google.com/search?tbm=shop&q=schwinn+810+gps) out there, however the software is limited to MS Windows and is [quite ugly](http://www.amazon.com/Schwinn-Tracking-Heart-Rate-Monitor/product-reviews/B006JPBALS/).

## Idea ##

All looks like [USBXpress Development Tools](http://www.silabs.com/products/mcu/Pages/USBXpress.aspx)
from Silicon Labs was used to communicate via USB-UART bridge [cp2102](http://www.silabs.com/pages/DownloadDoc.aspx?FILEURL=Support%20Documents/TechnicalDocs/CP2102.pdf).

It seems feasible to write a proxy and transcribe all communication between the software on Windows host and device behind USB-UART bridge.

Once protocol and data format are established, code can be written to fetch data.

There are choices as how to organize things. At first it seems natural to use a database to store all results.
However the question is what DB to use? Or shall we use *ODBC* to support virtually all?
If we use *sqlite*, we can access data with HTML5.

At the end I came to conclusion that there is nothing better than plain *CSV* files named after tracks.
All can be enumerated, some deleted, are human-readable, and can be accessed from other software easily.

The problem would be how to get overall statistics?
Like it would be sweet to use [R](http://www.r-project.org/) to see trends in progress across multiple runs.

## Vision

In the end I'd like to see everything modularized such that
same code can be reused with GUI for download progress, or built into a larger app.

## Implementation

Right now there are few independent components (with some code duplication like in download.py and settings.py :( )

- download.py is the main program to extract tracks, laps, points
- settings.py extracts all settings that can be fetched, like time zone threshold, user information, etc
- babelize.cmd is a hook script that optionally can be called by donload.py.
  It contains commands to execute for each track fetched.
- schwinn810.cmd is a convenience script to reduce amount of typing necessary to provide download.py with options
- csv2tcx.py converts laps & points into a single TCX file (gpsbabel lacks laps support)
- tcx2garmin, mmr_uploader are "templates" on how TCX could be uploaded automatically from babelize.cmd . For now, refer to source code.

Batch/shell scripts babelize and schwinn810 can be renamed for convenience.

## Build

### Just using up-to-date code

At these early stages, I'd recommend to use python source code and do not do compilation into binaries.
However, if you don't feel like installing tons of stuff on Windows, refer to download section.
I upload binary builds for MS Windows from time to time.

### To make Windows redistributable

1. Install Python 2.7 (preffered) or 3.2, pip, pyserial, cx_Freeze, and pytz.
2. ~~Execute `cxfreeze --compress --include-modules serial.win32 download.py --target-dir dist`~~
   Refer to [setup.py](https://github.com/mlt/schwinn810/blob/master/src/setup.py) and distutils manual on how to build

## Tasks

At this point one should not expect an exact copy of software for other OSes.

1. <del> Code proxy and transcribe communication making it possible for others to develop software independently.</del>
2. Improve [data format](https://github.com/mlt/schwinn810/wiki/Data-Format) details.
3. <del>Write some python (?) code that dumps data from serial port into *CSV*</del>
4. ~~Make it more [unicsv](http://www.gpsbabel.org/htmldoc-development/fmt_unicsv.html)-friendly so [gpsbabel](http://www.gpsbabel.org) can convert data to [GPX](http://www.gpsbabel.org/htmldoc-development/fmt_gpx.html) and/or [TCX](http://www.gpsbabel.org/htmldoc-development/fmt_gtrnctr.html).~~
4. Write some GUI, R code
5. Export to various web sites
6. Move command line options to a configuration file and **make things debconf friendly**