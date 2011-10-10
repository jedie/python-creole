#!/usr/bin/env python
# coding: utf-8

"""
    distutils setup
    ~~~~~~~~~~~~~~~

    :copyleft: 2009-2011 by the python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals
import os
import sys

from setuptools import setup, find_packages

from creole import VERSION_STRING
from creole.setup_utils import get_long_description


PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_authors():
    try:
        f = file(os.path.join(PACKAGE_ROOT, "AUTHORS"), "r")
        authors = [l.strip(" *\r\n") for l in f if l.strip().startswith("*")]
        f.close()
    except Exception as err:
        authors = "[Error: %s]" % err
    return authors


setup(
    name='python-creole',
    version=VERSION_STRING,
    description='python-creole is an open-source (GPL) markup converter in pure Python for: creole2html, html2creole, html2ReSt, html2textile',
    long_description=get_long_description(PACKAGE_ROOT),
    author=get_authors(),
    author_email="python-creole@jensdiemer.de",
    maintainer="Jens Diemer",
    url='http://code.google.com/p/python-creole/',
    packages=find_packages(),
    include_package_data=True, # include package data under svn source control
    data_files=[("", ["README.creole"])], # README used in unittest test_setup_utils.py
    zip_safe=False,
    classifiers=[
#        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    test_suite="creole.tests.run_all_tests",
)
