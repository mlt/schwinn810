#!/usr/bin/env python

import unittest
from schwinn810 import Device, Writer
import os
from os.path import join, dirname
from shutil import rmtree
import logging

_log = logging.getLogger(__name__)

class TestCrestaAlikeParser(unittest.TestCase):
    """ Tests for original Cresta """

    def setUp(self):
        logging.basicConfig(level=logging.WARNING)
        self.dir = dirname(__file__)
        self.tmp = join(self.dir, "tmp")
        self.dump = join(self.dir, "schwinn810_120713_2.bin")
        try:
            os.mkdir(self.tmp)
        except:
            pass

    def tearDown(self):
        rmtree(self.tmp)

    def test_default(self):
        d = Device(self.dump, False)
        w = Writer(self.tmp)
        d.read(w, None)

    def test_progress(self):
        from schwinn810 import TextProgress
        d = Device(self.dump, False)
        w = Writer(self.tmp)
        p = TextProgress()  # default progress
        d.read(w, p)

    def test_sqlwriter(self):
        from schwinn810.extra.writer_sqlite import SQLiteWriter
        d = Device(self.dump, False)
        w = SQLiteWriter(os.path.join(self.tmp, "out.db"), None)
        d.read(w, None)

if __name__ == '__main__':
    unittest.main()
