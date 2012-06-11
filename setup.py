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

from setuptools import setup, find_packages, Command

from creole import VERSION_STRING
from creole.setup_utils import get_long_description


PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_authors():
    try:
        f = file(os.path.join(PACKAGE_ROOT, "AUTHORS"), "r")
        authors = [l.strip(" *\r\n") for l in f if l.strip().startswith("*")]
        f.close()
    except Exception:
        evalue = sys.exc_info()[1]
        authors = "[Error: %s]" % evalue
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
    zip_safe=True, # http://packages.python.org/distribute/setuptools.html#setting-the-zip-safe-flag
    keywords="creole markup creole2html html2creole rest2html html2rest html2textile",
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
#        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Utilities",
    ],
    test_suite="creole.tests.get_test_suite",
)
