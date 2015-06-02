#!/usr/bin/env python
# coding: utf-8

"""
    unittest for CLI
    ~~~~~~~~~~~~~~~~

    :copyleft: 2013-2015 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import subprocess
import unittest
import sys
import os
import tempfile

from creole.tests.utils.base_unittest import BaseCreoleTest
from creole import VERSION_STRING
from creole.tests.utils.unittest_subprocess import SubprocessMixin

CMDS = ("creole2html", "html2creole", "html2rest", "html2textile")


class CreoleCLITests(BaseCreoleTest, SubprocessMixin):
    def _test_convert(self, source_content, dest_content, cli_str, verbose=True):
        assert isinstance(source_content, bytes), type(source_content)
        assert isinstance(dest_content, bytes), type(dest_content)

        source_file = tempfile.NamedTemporaryFile()
        sourcefilepath = source_file.name
        source_file.write(source_content)
        source_file.seek(0)

        dest_file = tempfile.NamedTemporaryFile()
        destfilepath = dest_file.name

        stdout=(
            "Convert '%(src)s' to '%(dst)s' with %(prog)s (codec: utf-8)\n"
            "done. '%(dst)s' created."
        ) % {
            "prog": cli_str,
            "src": sourcefilepath,
            "dst": destfilepath,
        }

        self.assertSubprocess(
            popen_args=[cli_str, sourcefilepath, destfilepath],
            retcode=0, stdout=stdout,
            verbose=False,
        )

        dest_file.seek(0)
        result_content = dest_file.read()

        result_content = result_content.decode("utf-8")
        dest_content = dest_content.decode("utf-8")
        self.assertEqual(result_content, dest_content)

    def test_version(self):
        for cmd in CMDS:
            version_info = "%s from python-creole v%s" % (
                cmd, VERSION_STRING
            )
            self.assertSubprocess(
                popen_args=[cmd, "--version"],
                retcode=0,
                stdout=version_info,
                verbose=False,
            )

    def test_creole2html(self):
        self._test_convert(
            source_content=b"= test creole2html =",
            dest_content=b"<h1>test creole2html</h1>",
            cli_str="creole2html",
        )

    def test_html2creole(self):
        self._test_convert(
            source_content=b"<h1>test html2creole</h1>",
            dest_content=b"= test html2creole",
            cli_str="html2creole",
        )

    def test_html2rest(self):
        self._test_convert(
            source_content=b"<h1>test html2rest</h1>",
            dest_content=(b"==============\n"
                          b"test html2rest\n"
                          b"=============="
            ),
            cli_str="html2rest",
        )

    def test_html2textile(self):
        self._test_convert(
            source_content=b"<h1>test html2textile</h1>",
            dest_content=b"h1. test html2textile",
            cli_str="html2textile",
        )


if __name__ == '__main__':
    unittest.main()
