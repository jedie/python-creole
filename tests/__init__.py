# coding: utf-8

from __future__ import division, absolute_import, print_function, unicode_literals

import unittest

from . import run_all_tests as all_tests

def run_all_tests():
    suite = unittest.findTestCases(all_tests)
    return suite
