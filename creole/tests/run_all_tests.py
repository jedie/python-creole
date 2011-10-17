#!/usr/bin/env python
# coding: utf-8

"""
    run all unittests
    ~~~~~~~~~~~~~~~~~
    
    for e.g.:
        coverage run creole/tests/run_all_tests.py

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from creole.tests import run_all_doctests, run_unittests


if __name__ == '__main__':
    run_all_doctests()
    run_unittests()
