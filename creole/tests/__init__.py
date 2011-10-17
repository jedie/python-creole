#!/usr/bin/env python
# coding: utf-8

"""
    python-creole unittests
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import unittest
from unittest.runner import TextTestRunner

from creole.tests import all_tests


def get_test_suite():
    """
    return the unittest.TestSuite for setup.py
    """
    suite = unittest.findTestCases(all_tests)
    return suite


if __name__ == '__main__':
    suite = get_test_suite()

#    for entry in suite:
#        print(entry)

    runner = TextTestRunner()
    runner.run(suite)

