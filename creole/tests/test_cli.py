#!/usr/bin/env python
# coding: utf-8

"""
    unittest for CLI
    ~~~~~~~~~~~~~~~~

    :copyleft: 2013 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import unittest
import sys
import tempfile

from creole.tests.utils.base_unittest import BaseCreoleTest
from creole.cmdline import cli_creole2html, cli_html2creole, cli_html2rest, \
    cli_html2textile


class CreoleCLITests(BaseCreoleTest):
    def setUp(self):
        super(CreoleCLITests, self).setUp()
        self._old_argv = sys.argv[:]
    def tearDown(self):
        super(CreoleCLITests, self).tearDown()
        sys.argv = self._old_argv

    def _test_convert(self, source_content, dest_content, cli_func):
        source_file = tempfile.NamedTemporaryFile()
        sourcefilepath = source_file.name
        source_file.write(source_content)
        source_file.seek(0)

        dest_file = tempfile.NamedTemporaryFile()
        destfilepath = dest_file.name

        sys.argv += [sourcefilepath, destfilepath]
        cli_func()

        dest_file.seek(0)
        result_content = dest_file.read()

#         print(dest_content)
        self.assertEqual(result_content, dest_content)

    def test_creole2html(self):
        self._test_convert(
            source_content=b"= test creole2html =",
            dest_content=b"<h1>test creole2html</h1>",
            cli_func=cli_creole2html
        )

    def test_html2creole(self):
        self._test_convert(
            source_content=b"<h1>test html2creole</h1>",
            dest_content=b"= test html2creole",
            cli_func=cli_html2creole
        )

    def test_html2rest(self):
        self._test_convert(
            source_content=b"<h1>test html2rest</h1>",
            dest_content=(b"==============\n"
                "test html2rest\n"
                "=============="
            ),
            cli_func=cli_html2rest
        )

    def test_html2textile(self):
        self._test_convert(
            source_content=b"<h1>test html2textile</h1>",
            dest_content=b"h1. test html2textile",
            cli_func=cli_html2textile
        )

if __name__ == '__main__':
    unittest.main()
