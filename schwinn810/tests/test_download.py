#!/usr/bin/env python

import unittest
from schwinn810.download import main as download
import os
from os.path import join, dirname, exists
from shutil import rmtree
import logging

_log = logging.getLogger(__name__)

class TestDownload(unittest.TestCase):
    """ Test downloader """

    def setUp(self):
        logging.basicConfig(level=logging.WARNING)
        self.dir = dirname(__file__)
        self.tmp = join(self.dir, "tmp")
        self.dump = join(self.dir, "cresta.bin")
        try:
            os.mkdir(self.tmp)
        except:
            pass

    def tearDown(self):
        rmtree(self.tmp)

    def test_default(self):
        download(['--port', self.dump,
                  '--dir', self.tmp,
                  '--subfolder', '%Y',
                  '--progress', 'none'])
        self.assertTrue(exists(join(self.tmp, '2012')))

if __name__ == '__main__':
    unittest.main()
