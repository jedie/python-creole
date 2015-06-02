# coding: utf-8

"""
    unittest
    ~~~~~~~~

    :copyleft: 2015 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import unittest
import sys
import os

from creole.tests.utils.unittest_subprocess import SubprocessMixin


class TestSubprocessMixin(unittest.TestCase, SubprocessMixin):
    def test_find_executable(self):
        filepath = self.find_executable("python")
        if not hasattr(self, "assertRegex"): # New in version 3.1
            self.assertRegex = self.assertRegexpMatches
        self.assertRegex(filepath, ".*?python.*?")

    def test_executable_not_exists(self):
        with self.assertRaisesRegexp(AssertionError, """Program "doesn't exists!" not found in:.*"""):
            self.find_executable("doesn't exists!")

    def test_executable_with_path(self):
        msg = "'%s' unexpectedly found in '%s'" % (
            os.sep, sys.executable
        )
        with self.assertRaisesRegexp(AssertionError, msg):
            self.find_executable(sys.executable)

    def test_subprocess(self):
        popen_args, retcode, stdout = self.subprocess(
            popen_args=[sys.executable, "-c", "import sys;sys.stdout.write('to stdout')"],
            verbose=False
        )
        self.assertEqual(stdout, "to stdout")
        self.assertEqual(retcode, 0)

    def test_assertSubprocess(self):
        code = (
            "import sys;"
            "sys.stdout.write('to stdout 1\\n');"
            "sys.stdout.flush();"
            "sys.stderr.write('to stderr 1\\n');"
            "sys.stderr.flush();"
            "sys.stdout.write('to stdout 2\\n');"
            "sys.stdout.flush();"
            "sys.stderr.write('to stderr 2\\n');"
            "sys.stderr.flush();"
        )
        self.assertSubprocess(
            popen_args=(sys.executable, "-c", code),
            retcode=0,
            stdout=(
                "to stdout 1\n"
                "to stderr 1\n"
                "to stdout 2\n"
                "to stderr 2\n"
            ),
            verbose=True
        )

