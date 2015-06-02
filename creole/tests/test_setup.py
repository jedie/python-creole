#!/usr/bin/env python
# coding: utf-8

"""
    unittest for CLI
    ~~~~~~~~~~~~~~~~

    :copyleft: 2013-2015 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import unittest
import sys
import os

import creole
from creole.tests.utils.unittest_subprocess import SubprocessMixin


class TestSetup(unittest.TestCase, SubprocessMixin):
    @classmethod
    def setUpClass(cls):
        cls.setup_path = os.path.join(os.path.dirname(creole.__file__), "..", "setup.py")

    def test_setup_path(self):
        if not os.path.isfile(self.setup_path):
            self.fail("Can't find setup.py: %r doesn't exist" % self.setup_path)

    def test_version(self):
        self.assertSubprocess(
            popen_args=(sys.executable, self.setup_path, "--version"),
            retcode=0,
            stdout=creole.VERSION_STRING,
            verbose=True
        )

    def test_nose_hint(self):
        popen_args, retcode, stdout = self.subprocess(
            popen_args=(sys.executable, self.setup_path, "test"),
            verbose=False,
        )
        self.assertIn("Please use 'nosetests'", stdout)
        self.assertNotEqual(retcode, 0)


