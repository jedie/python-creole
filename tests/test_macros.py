# coding: utf-8


"""
    Creole unittest macros
    ~~~~~~~~~~~~~~~~~~~~~~
    
    Note: all mecro functions must return unicode!
    
    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


def test_macro1(**kwargs):
    """
    >>> test_macro1(foo="bar")
    u"[test macro1 - kwargs: foo='bar']"
    
    >>> test_macro1()
    u'[test macro1 - kwargs: ]'
    
    >>> test_macro1(a=1,b=2)
    u'[test macro1 - kwargs: a=1,b=2]'
    """
    kwargs = u','.join([u'%s=%r' % (k, v) for k, v in sorted(kwargs.items())])
    return u"[test macro1 - kwargs: %s]" % kwargs

def test_macro2(char, text):
    """
    >>> test_macro2(char=u"|", text=u"a\\nb")
    u'a|b'
    """
    return char.join(text.split())


if __name__ == "__main__":
    import doctest
    print doctest.testmod()
