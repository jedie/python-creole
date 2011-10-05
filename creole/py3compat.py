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

from __future__ import division, absolute_import, print_function, unicode_literals

import sys
import doctest
import re

# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3


if PY3:
    TEXT_TYPE = str
    BINARY_TYPE = bytes
else:
    TEXT_TYPE = unicode
    BINARY_TYPE = str

    # Simple remove 'u' from python 2 unicode repr string
    # See also:
    # http://bugs.python.org/issue3955
    # http://www.python-forum.de/viewtopic.php?f=1&t=27509 (de)
    origin_OutputChecker = doctest.OutputChecker
    class OutputChecker2(origin_OutputChecker):
        def check_output(self, want, got, optionflags):
            got = got.replace("u'", "'").replace('u"', '"')
            return origin_OutputChecker.check_output(self, want, got, optionflags)
    doctest.OutputChecker = OutputChecker2


def repr2(obj):
    """
    Don't mark unicode strings with u in Python 2
    """
    if not PY3:
        return repr(obj).lstrip("u")
    else:
        return repr(obj)


