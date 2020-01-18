#!/usr/bin/env python
# coding: utf-8

"""
    unittest for CLI
    ~~~~~~~~~~~~~~~~

    :copyleft: 2013-2015 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import os
import sys
import unittest

import creole
from creole.tests.utils.unittest_subprocess import SubprocessMixin


class TestSetup(unittest.TestCase, SubprocessMixin):
    @classmethod
    def setUpClass(cls):
        cls.setup_path = os.path.join(os.path.dirname(creole.__file__), "..", "setup.py")

    def test_setup_path(self):
        if not os.path.isfile(self.setup_path):
            self.fail(f"Can't find setup.py: {self.setup_path!r} doesn't exist")

    def test_version(self):
        self.assertSubprocess(
            popen_args=(sys.executable, self.setup_path, "--version"),
            retcode=0,
            stdout=creole.VERSION_STRING,
            verbose=True
        )
