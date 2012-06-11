#!/usr/bin/env python
# coding: utf-8

"""
    unittest for setup_utils
    ~~~~~~~~~~~~~~~~~~~~~~~~
    
    https://code.google.com/p/python-creole/wiki/UseInSetup

    :copyleft: 2011-2012 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import unittest
import os

import creole
from creole.setup_utils import get_long_description
from creole.tests.utils.base_unittest import BaseCreoleTest
from creole.py3compat import BINARY_TYPE, PY3, TEXT_TYPE
import tempfile


CREOLE_PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(creole.__file__), ".."))
TEST_README_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_README_FILENAME = "test_README.creole"


class SetupUtilsTests(BaseCreoleTest):
    def test_creole_package_path(self):
        self.assertTrue(
            os.path.isdir(CREOLE_PACKAGE_ROOT),
            "CREOLE_PACKAGE_ROOT %r is not a existing direcotry!" % CREOLE_PACKAGE_ROOT
        )
        filepath = os.path.join(CREOLE_PACKAGE_ROOT, "README.creole")
        self.assertTrue(
            os.path.isfile(filepath),
            "README file %r not found!" % filepath
        )

    def test_get_long_description_without_raise_errors(self):
        long_description = get_long_description(CREOLE_PACKAGE_ROOT, raise_errors=False)
        self.assertIn("=====\nabout\n=====\n\n", long_description)
        # Test created ReSt code
        from creole.rest2html.clean_writer import rest2html
        html = rest2html(long_description)
        self.assertIn("<h1>about</h1>\n", html)

    def test_get_long_description_with_raise_errors(self):
        long_description = get_long_description(CREOLE_PACKAGE_ROOT, raise_errors=True)
        self.assertIn("=====\nabout\n=====\n\n", long_description)

    def _tempfile(self, content):
        fd = tempfile.NamedTemporaryFile()
        path, filename = os.path.split(fd.name)

        fd.write(content)
        fd.seek(0)
        return path, filename, fd

    def test_tempfile_without_error(self):
        path, filename, fd = self._tempfile(b"== noerror ==")
        try:
            long_description = get_long_description(path, filename, raise_errors=True)
            self.assertEqual(long_description, "-------\nnoerror\n-------")
        finally:
            fd.close()
            
    def test_get_long_description_error_handling(self):
        """
        Test if get_long_description will raised a error, if description
        produce a ReSt error.
        
        We test with this error:
        <string>:102: (ERROR/3) Document or section may not begin with a transition.
        """
        path, filename, fd = self._tempfile(b"----")
        try:
            self.assertRaises(SystemExit, get_long_description, path, filename, raise_errors=True)
        finally:
            fd.close()

    def test_wrong_path_without_raise_errors(self):
        self.assertEqual(
            get_long_description("wrong/path", raise_errors=False).replace("u'", "'"),
            "[Error: [Errno 2] No such file or directory: 'wrong/path/README.creole']\n"
        )

    def test_wrong_path_with_raise_errors(self):
        self.assertRaises(IOError, get_long_description, "wrong/path", raise_errors=True)

    def test_readme_encoding(self):
        long_description = get_long_description(TEST_README_DIR, filename=TEST_README_FILENAME, raise_errors=True)

        if PY3:
            self.assertTrue(isinstance(long_description, TEXT_TYPE))
        else:
            self.assertTrue(isinstance(long_description, BINARY_TYPE))

        txt = "German Umlaute: ä ö ü ß Ä Ö Ü"
        if not PY3:
            txt = txt.encode("utf-8")
        self.assertIn(txt, long_description)

if __name__ == '__main__':
    unittest.main()
