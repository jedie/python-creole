#!/usr/bin/env python
# coding: utf-8

"""
    distutils setup
    ~~~~~~~~~~~~~~~

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate$
    $Rev$
    $Author$

    :copyleft: 2009 by the python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
import sys

from setuptools import setup, find_packages

from creole import VERSION_STRING


def get_authors():
    authors = []
    f = file("AUTHORS", "r")
    for line in f:
        if line.startswith('*'):
            authors.append(line[1:].strip())
    f.close()
    return authors

def get_long_description():
    f = file("README", "r")
    long_description = f.read()
    f.close()
    long_description.strip()
    return long_description


setup(
    name='python-creole',
    version=VERSION_STRING,
    description='python-creole is an open-source creole2html and html2creole converter in pure Python.',
    long_description = get_long_description(),
    author = get_authors(),
    maintainer = "Jens Diemer",
    url='http://code.google.com/p/python-creole/',
    packages=find_packages(),
    include_package_data=True, # include package data under svn source control
    zip_safe=True,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Operating System :: OS Independent",
    ]
)
