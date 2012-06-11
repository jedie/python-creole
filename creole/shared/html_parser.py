# coding: utf-8

"""
    Patched version of HTMLParser with patch from:
        http://bugs.python.org/issue670664
    See also:
        https://github.com/gregmuellegger/django/issues/1
        
    It was fixed with:
        http://www.python.org/download/releases/2.7.3/
        http://www.python.org/download/releases/3.2.3/
    see also:
        http://bugs.python.org/issue670664#msg146770
"""


try:
    import HTMLParser as OriginHTMLParser
except ImportError:
    from html import parser as OriginHTMLParser # python 3


if hasattr(OriginHTMLParser, "cdata_elem"):
    # Current python version has 
    HTMLParser = OriginHTMLParser
else:
    # Current python version is not patched -> use own patched version
    from creole.shared.HTMLParsercompat import HTMLParser
