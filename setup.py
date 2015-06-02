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


if "publish" in sys.argv:
    try:
        # Test if wheel is installed, otherwise the user will only see:
        #   error: invalid command 'bdist_wheel'
        import wheel
    except ImportError as err:
        print("\nError: %s" % err)
        print("\nMaybe https://pypi.python.org/pypi/wheel is not installed or virtualenv not activated?!?")
        print("e.g.:")
        print("    ~/your/env/$ source bin/activate")
        print("    ~/your/env/$ pip install wheel")
        sys.exit(-1)

    import subprocess
    args = [sys.executable or "python", "setup.py", "sdist", "bdist_wheel", "upload"]
    print("\nCall: %r\n" %  " ".join(args))
    subprocess.call(args)

    print("\nDon't forget to tag this version, e.g.:")
    print("\tgit tag v%s" % VERSION_STRING)
    print("\tgit push --tags")
    sys.exit()


if "test" in sys.argv or "nosetests" in sys.argv:
    """
    nose is a optional dependency, so test import.
    Otherwise the user get only the error:
        error: invalid command 'nosetests'
    """
    try:
        import nose
    except ImportError as err:
        print("\nError: Can't import 'nose': %s" % err)
        print("\nMaybe 'nose' is not installed or virtualenv not activated?!?")
        print("e.g.:")
        print("    ~/your/env/$ source bin/activate")
        print("    ~/your/env/$ pip install nose")
        print("    ~/your/env/$ ./setup.py nosetests\n")
        sys.exit(-1)
    else:
        if "test" in sys.argv:
            print("\nPlease use 'nosetests' instead of 'test' to cover all tests!\n")
            print("e.g.:")
            print("     $ ./setup.py nosetests\n")
            sys.exit(-1)


def get_authors():
    try:
        with open(os.path.join(PACKAGE_ROOT, "AUTHORS"), "r") as f:
            authors = [l.strip(" *\r\n") for l in f if l.strip().startswith("*")]
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
    url='https://github.com/jedie/python-creole/',
    packages=find_packages(),
    include_package_data=True, # include package data under svn source control
    data_files=[("", ["README.creole"])], # README used in unittest test_setup_utils.py
    entry_points={
        "console_scripts": [
            "creole2html = creole.cmdline:cli_creole2html",
            "html2creole = creole.cmdline:cli_html2creole",
            "html2rest = creole.cmdline:cli_html2rest",
            "html2textile = creole.cmdline:cli_html2textile",
        ],
    },
    tests_require=[
        "nose", # https://pypi.python.org/pypi/nose
    ],
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
    test_suite="nose.collector",
)
