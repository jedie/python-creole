# coding: utf-8

"""
    Helper to support Python v2 and v3
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Some ideas borrowed from six
    
    See also:
        http://python3porting.com
        https://bitbucket.org/gutworth/six/src/tip/six.py
        http://packages.python.org/six/
"""

import sys

# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3


if PY3:
    TEXT_TYPE = str
    BINARY_TYPE = bytes
else:
    TEXT_TYPE = unicode
    BINARY_TYPE = str


def repr2(obj):
    """
    Don't mark unicode strings with u in Python 2
    """
    if not PY3:
        return repr(obj).lstrip("u")
    else:
        return repr(obj)
