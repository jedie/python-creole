#!/usr/bin/env python
# coding: utf-8

"""
    collects all existing unittests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2008-2012 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

from doctest import testmod
import os
import sys
import time
import unittest

try:
    import creole
except ImportError as err:
    # running tests, but creole is not in sys.path
    raise ImportError("Seems that pyhton-creole is not installed, correctly: %s" % err)

from creole.tests.test_creole2html import TestCreole2html, TestCreole2htmlMarkup, TestStr2Dict, TestDict2String
from creole.tests.test_cross_compare_all import CrossCompareTests
from creole.tests.test_cross_compare_creole import CrossCompareCreoleTests
from creole.tests.test_cross_compare_rest import CrossCompareReStTests
from creole.tests.test_cross_compare_textile import CrossCompareTextileTests
from creole.tests.test_html2creole import TestHtml2Creole, TestHtml2CreoleMarkup
from creole.tests.test_rest2html import ReSt2HtmlTests
from creole.tests.test_setup_utils import SetupUtilsTests
from creole.tests.test_utils import UtilsTests
from creole.tests.utils.utils import MarkupTest

import creole.tests


SKIP_DIRS = (".settings", ".git", "dist", "python_creole.egg-info")
SKIP_FILES = ("setup.py", "test.py")


if "-v" in sys.argv or "--verbosity" in sys.argv:
    VERBOSE = 2
elif "-q" in sys.argv or "--quite" in sys.argv:
    VERBOSE = 0
else:
    VERBOSE = 1


def run_all_doctests(verbosity=None):
    """
    run all python-creole DocTests
    """
    start_time = time.time()
    if verbosity is None:
        verbosity = VERBOSE

    path = os.path.abspath(os.path.dirname(creole.__file__))
    if verbosity >= 2:
        print("")
        print("_" * 79)
        print("Running %r DocTests:\n" % path)

    total_files = 0
    total_doctests = 0
    total_attempted = 0
    total_failed = 0
    for root, dirs, filelist in os.walk(path, followlinks=True):
        for skip_dir in SKIP_DIRS:
            if skip_dir in dirs:
                dirs.remove(skip_dir) # don't visit this directories

        for filename in filelist:
            if not filename.endswith(".py"):
                continue
            if filename in SKIP_FILES:
                continue

            total_files += 1

            sys.path.insert(0, root)
            try:
                m = __import__(filename[:-3])
            except ImportError as err:
                if verbosity >= 2:
                    print("***DocTest import %s error*** %s" % (filename, err))
            except Exception as err:
                if verbosity >= 2:
                    print("***DocTest %s error*** %s" % (filename, err))
            else:
                failed, attempted = testmod(m)
                total_attempted += attempted
                total_failed += failed
                if attempted or failed:
                    total_doctests += 1

                if attempted and not failed:
                    filepath = os.path.join(root, filename)
                    if verbosity <= 1:
                        sys.stdout.write(".")
                    elif verbosity >= 2:
                        print("DocTest in %s OK (failed=%i, attempted=%i)" % (
                            filepath, failed, attempted
                        ))
            finally:
                del sys.path[0]

    duration = time.time() - start_time
    print("")
    print("-"*70)
    print("Ran %i DocTests from %i files in %.3fs: failed=%i, attempted=%i\n\n" % (
        total_doctests, total_files, duration, total_failed, total_attempted
    ))


def run_unittests(verbosity=None):
    """
    run all python-creole unittests with unittest CLI TestProgram()
    """
    if verbosity is None:
        verbosity = VERBOSE

    if verbosity >= 2:
        print("")
        print("_" * 79)
        print("Running Unittests:\n")

    if sys.version_info >= (2, 7):
        unittest.main(verbosity=verbosity)
    else:
        unittest.main()


if __name__ == '__main__':
    # for e.g.:
    #    coverage run creole/tests/all_tests.py
    run_all_doctests()
    run_unittests()
