#!/usr/bin/env python
# coding: utf-8

"""
    unittest for setup_utils
    ~~~~~~~~~~~~~~~~~~~~~~~~

    https://code.google.com/p/python-creole/wiki/UseInSetup

    :copyleft: 2011-2014 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""



import os
import tempfile
import unittest
import warnings

import creole
from creole.setup_utils import get_long_description
from creole.tests.utils.base_unittest import BaseCreoleTest

try:
    import docutils

    DOCUTILS = True
except ImportError:
    DOCUTILS = False


CREOLE_PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(creole.__file__), ".."))
TEST_README_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_README_FILENAME = "test_README.creole"


# TODO: Use @unittest.skipIf if python 2.6 will be not support anymore.
# @unittest.skipIf(DOCUTILS == False, "docutils not installed.")
class SetupUtilsTests(BaseCreoleTest):
    def run(self, *args, **kwargs):
        # TODO: Remove if python 2.6 will be not support anymore.
        if DOCUTILS == False:
            warnings.warn("Skip SetupUtilsTests, because 'docutils' not installed.")
            return
        return super(SetupUtilsTests, self).run(*args, **kwargs)

    def test_creole_package_path(self):
        self.assertTrue(
            os.path.isdir(CREOLE_PACKAGE_ROOT),
            f"CREOLE_PACKAGE_ROOT {CREOLE_PACKAGE_ROOT!r} is not a existing direcotry!",
        )
        filepath = os.path.join(CREOLE_PACKAGE_ROOT, "README.creole")
        self.assertTrue(os.path.isfile(filepath), f"README file {filepath!r} not found!")

    def test_get_long_description_without_raise_errors(self):
        long_description = get_long_description(CREOLE_PACKAGE_ROOT, raise_errors=False)
        self.assertIn("=====\nabout\n=====\n\n", long_description)
        # Test created ReSt code
        from creole.rest_tools.clean_writer import rest2html

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

    def test_get_long_description_error_handling2(self):
        """
        Test if get_long_description will raised a error, if description
        produce a ReSt error.

        We test with this error:
        SystemExit: ReSt2html error: link scheme not allowed
        """
        path, filename, fd = self._tempfile(b"[[foo://bar]]")
        #         print(get_long_description(path, filename, raise_errors=True))
        try:
            self.assertRaises(SystemExit, get_long_description, path, filename, raise_errors=True)
        finally:
            fd.close()

    def test_wrong_path_without_raise_errors(self):
        self.assertEqual(
            get_long_description("wrong/path", raise_errors=False).replace("u'", "'"),
            "[Error: [Errno 2] No such file or directory: 'wrong/path/README.creole']\n",
        )

    def test_wrong_path_with_raise_errors(self):
        self.assertRaises(IOError, get_long_description, "wrong/path", raise_errors=True)

    def test_readme_encoding(self):
        long_description = get_long_description(TEST_README_DIR, filename=TEST_README_FILENAME, raise_errors=True)

        self.assertTrue(isinstance(long_description, str))

        txt = "German Umlaute: ä ö ü ß Ä Ö Ü"
        self.assertIn(txt, long_description)


if __name__ == "__main__":
    unittest.main()
