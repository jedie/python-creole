#!/usr/bin/env python
# coding: utf-8

"""
    run all unittests
    ~~~~~~~~~~~~~~~~~

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from doctest import testmod
import os
import sys
import unittest

from tests.test_creole2html import TestCreole2html, TestCreole2htmlMarkup
from tests.test_cross_compare_all import CrossCompareTests
from tests.test_cross_compare_creole import CrossCompareCreoleTests
from tests.test_cross_compare_rest import CrossCompareReStTests
from tests.test_cross_compare_textile import CrossCompareTextileTests
from tests.test_html2creole import TestHtml2Creole, TestHtml2CreoleMarkup
from tests.test_rest2html import ReSt2HtmlTests
from tests.test_utils import UtilsTests
from tests.utils.utils import MarkupTest


SKIP_DIRS = (".settings", ".git", "dist", "python_creole.egg-info")
SKIP_FILES = ("setup.py", "test.py")


def run_all_doctests():
    print
    print "_" * 79
    print "Running DocTests:\n"

    for root, dirs, filelist in os.walk("../", followlinks=True):
        for skip_dir in SKIP_DIRS:
            if skip_dir in dirs:
                dirs.remove(skip_dir) # don't visit this directories

        for filename in filelist:
            if not filename.endswith(".py"):
                continue
            if filename in SKIP_FILES:
                continue

            sys.path.insert(0, root)
            m = __import__(filename[:-3])
            del sys.path[0]

            failed, attempted = testmod(m)
            if attempted and not failed:
                filepath = os.path.join(root, filename)
                print "DocTest in %s OK (failed=%i, attempted=%i)" % (
                    filepath, failed, attempted
                )


if __name__ == '__main__':
    run_all_doctests()

    print
    print "_" * 79
    print "Running Unittests:\n"

    unittest.main(
        #verbosity=99
    )
#elif len(sys.argv) > 1 and sys.argv[1] == "test":
#    # e.g.: .../python-creole$ ./setup.py test
#    run_all_doctests()
