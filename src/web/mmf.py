#!/usr/bin/env python
# -*- coding: utf-8; mode: python; mode: ropemacs -*-

# Copyright (c) 2012, Mikhail Titov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import antd.plugin as plugin
import requests
import re
import logging
import os

_log = logging.getLogger(__name__)

class MMF(plugin.Plugin):

    username = None
    password = None

    logged_in = False
    login_invalid = False

    def __init__(self):
        self.url = 'www.mapmyrun.com'

    def data_available(self, device_sn, format, files):
        if format not in ("tcx"): return files
        result = []
        try:
            for file in files:
                self.login()
                self.upload(format, file)
                result.append(file)
        except Exception:
            _log.warning("Failed to upload to MMF.", exc_info=True)
        finally:
            return result

    def login(self):
        if self.logged_in: return
        if self.login_invalid: raise InvalidLogin()

        payload = { 'username_login': self.username,
                    'password_login': self.password,
                    'action_type': 'login' }
        url = "http://{:s}/auth/login/".format(self.url)
        r = requests.get(url)
        # post login credentials
        _log.debug("Posting login credentials to MMF. username=%s", self.username)
        url = "https://{:s}/auth/login/".format(self.url)
        r = requests.post(url, data=payload, cookies=r.cookies)
        if 302 != r.status_code:
            raise InvalidLogin()
        # verify we're logged in
        _log.debug("Checking if login was successful.")
        username = r.cookies['_cache_username']
        if username == "":
            self.login_invalid = True
            raise InvalidLogin()
        elif username != self.username:
            _log.warning("Username mismatch, probably OK, if upload fails check user/pass. %s != %s" % (username, self.username))
        self.logged_in = True
        self.cookies = r.cookies
    
    def upload(self, format, file_name):
        url = "http://{:s}/workout/import/?source=file".format(self.url)
        r = requests.get(url, cookies=self.cookies)
        payload = { 'import_uuid': '', 'file_type': 'tcx' }
        base = os.path.basename(file_name)
        files = {'file': ( base, open(file_name, 'rb'))}
        r = requests.post(url, data=payload, files=files, cookies=r.cookies)

        # no need for BeautifulSoup just yet
        m = re.search('name="data_uuid" value="(.+)"', r.content)
        if m:
            payload = { 'activity_type': '16', # run/jog
                        'route_name': base,
                        'data_uuid': m.group(1) }
            _log.info("Uploading %s to MMF.", file_name) 
            r = requests.post(url, data=payload, cookies=r.cookies)
        else:
            raise Exception("data_uuid is missing in cookies")

class InvalidLogin(Exception): pass


def main():
    import argparse
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='MMF uploader.')
    parser.add_argument('--user', nargs=1, required=True,
                   help='Your MMF username')
    parser.add_argument('--password', nargs=1, required=True,
                   help='Your MMF password')
    parser.add_argument(dest='tcx', nargs='+',
                   help='TCX files to upload')
    args = parser.parse_args()

    m = MMF()
    m.username = args.user[0]
    m.password = args.password[0]
    m.data_available(None, 'tcx', args.tcx)

if __name__ == '__main__':
    main()
