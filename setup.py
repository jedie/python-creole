#!/usr/bin/env python
# coding: utf-8

"""
    distutils setup
    ~~~~~~~~~~~~~~~

    :copyleft: 2009-2011 by the python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
import sys

from setuptools import setup, find_packages

from creole import VERSION_STRING, creole2html, html2rest


PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_authors():
    try:
        f = file(os.path.join(PACKAGE_ROOT, "AUTHORS"), "r")
        authors = [l.strip(" *\r\n") for l in f if l.strip().startswith("*")]
        f.close()
    except Exception, err:
        authors = "[Error: %s]" % err
    return authors


def get_long_description():
    try:
        f = file(os.path.join(PACKAGE_ROOT, "README.creole"), "r")
        desc_creole = f.read()
        f.close()

        desc_creole = unicode(desc_creole, 'utf-8').strip()

        desc_html = creole2html(desc_creole)
        long_description = html2rest(desc_html)
    except Exception, err:
        if len(sys.argv) > 1 and sys.argv[1] in ("--long-description", "sdist"):
            raise
        long_description = "[Error: %s]" % err

    return long_description


setup(
    name='python-creole',
    version=VERSION_STRING,
    description='python-creole is an open-source (GPL) markup converter in pure Python for: creole2html, html2creole, html2ReSt, html2textile',
    long_description=get_long_description(),
    author=get_authors(),
    maintainer="Jens Diemer",
    url='http://code.google.com/p/python-creole/',
    packages=find_packages(),
    include_package_data=True, # include package data under svn source control
    zip_safe=True,
    classifiers=[
#        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Operating System :: OS Independent",
    ],
    test_suite="tests.run_all_tests",
)
