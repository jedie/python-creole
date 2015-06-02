# coding: utf-8


"""
    Creole unittest macros
    ~~~~~~~~~~~~~~~~~~~~~~
    
    Note: all mecro functions must return unicode!
    
    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from __future__ import division, absolute_import, print_function, unicode_literals

import json

def unittest_macro1(**kwargs):
    """
    >>> unittest_macro1(foo="bar")
    '[test macro1 - kwargs: foo="bar"]'
    
    >>> unittest_macro1()
    '[test macro1 - kwargs: ]'
    
    >>> unittest_macro1(a=1,b=2)
    '[test macro1 - kwargs: a=1,b=2]'
    """
    kwargs = ','.join(['%s=%s' % (k, json.dumps(v)) for k, v in sorted(kwargs.items())])
    return "[test macro1 - kwargs: %s]" % kwargs


def unittest_macro2(char, text):
    """
    >>> unittest_macro2(char="|", text="a\\nb")
    'a|b'
    """
    return char.join(text.split())

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())