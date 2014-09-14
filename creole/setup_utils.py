# coding: utf-8

"""
    utils for distutils setup
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Get README.creole as ReStructuredText on-the-fly for setup.long_description

    More information:
        https://code.google.com/p/python-creole/wiki/UseInSetup

    usage in setup.py e.g.:
    ---------------------------------------------------------------------------
    #!/usr/bin/env python
    # coding: utf-8

    import os
    import sys
    from setuptools import setup, find_packages

    PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

    try:
        from creole.setup_utils import get_long_description
    except ImportError:
        if "register" in sys.argv or "sdist" in sys.argv or "--long-description" in sys.argv:
            etype, evalue, etb = sys.exc_info()
            evalue = etype("%s - Please install python-creole >= v0.8 -  e.g.: pip install python-creole" % evalue)
            raise etype, evalue, etb
        long_description = None
    else:
        long_description = get_long_description(PACKAGE_ROOT)

    setup(
        ...
        long_description = long_description,
        ...
    )
    ---------------------------------------------------------------------------

    :copyleft: 2011-2014 by the python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import codecs
import os
import sys
import warnings

from creole import creole2html, html2rest
from creole.shared.unknown_tags import raise_unknown_node, transparent_unknown_nodes
from creole.py3compat import PY3


RAISE_ERRORS_ARGS = (
    "check", "register", "sdist", "bdist", "upload",
    "--long-description", "--restructuredtext",
)


def should_raise_errors():
    """
    Raise only errors, if one of RAISE_ERRORS_ARGS is in sys.argv
    or if no argument presents.
    """
    if len(sys.argv) == 1:
        return True

    for arg in RAISE_ERRORS_ARGS:
        if arg in sys.argv:
            return True
    return False


def get_long_description(package_root, filename="README.creole", raise_errors=None):
    """ read README file and convert it on-the-fly to ReStructuredText. """
    if raise_errors is None:
        raise_errors = should_raise_errors()

    if raise_errors:
        sys.stderr.write("Test creole2rest and raise an error, if rendering failed...\n")
        # raise a error if a unknown node found
        unknown_emit = raise_unknown_node
    else:
        # ignore unknown nodes
        unknown_emit = transparent_unknown_nodes

    filepath = os.path.join(package_root, filename)
    long_description_origin = ""
    try:
        # Read creole README
        f = codecs.open(filepath, "r", encoding="utf-8")
        long_description_origin = f.read().strip()
        f.close()

        # convert creole into html
        long_description_html = creole2html(long_description_origin)

        # convert html to ReSt
        long_description_rest_unicode = html2rest(
            long_description_html,
            emitter_kwargs={"unknown_emit":unknown_emit}
        )
        if PY3:
            long_description_rest = long_description_rest_unicode
        else:
            long_description_rest = long_description_rest_unicode.encode("utf-8")
    except Exception:
        if raise_errors:
            raise
        # Don't raise the error e.g. in ./setup install process
        evalue = sys.exc_info()[1]
        long_description_rest = "[Error: %s]\n%s" % (
            evalue, long_description_origin
        )
    else:
        if raise_errors:
            # Test created ReSt code like PyPi does it.
            from creole.rest2html.pypi_rest2html import pypi_rest2html
            try:
                pypi_rest2html(long_description_rest_unicode)
            except SystemExit as e:
                msg = "Error creole2rest self test failed: rest2html() exist with status code: %s\n" % e.args[0]
                sys.stderr.write(msg)
                sys.exit(msg)
            except Exception as e:
                sys.exit("ReSt2html error: %s" % e)
            else:
                if "check" in sys.argv:
                    print("Generating creole to ReSt to html, ok.")

    return long_description_rest


def _get_long_description(*args, **kwargs):
    msg = "'GetLongDescription' is deprecated, use 'get_long_description' instead."
    if should_raise_errors():
        raise DeprecationWarning(msg)
    else:
        warnings.warn(msg, DeprecationWarning)
    return get_long_description(*args, **kwargs)
GetLongDescription = _get_long_description # for backward-compatibility


if __name__ == "__main__":
    package_root = os.path.abspath("../")
    long_description = get_long_description(package_root)
    print(long_description)

