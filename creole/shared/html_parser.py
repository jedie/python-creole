# coding: utf-8

"""
    HTMLParser for Python 2.x and 3.x
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The HTMLParser has problems with the correct handling of <script>...</script>
    and <style>...</style> areas.
       
    It was fixed with v2.7.3 and 3.2.3, see:
        http://www.python.org/download/releases/2.7.3/
        http://www.python.org/download/releases/3.2.3/
    see also:
        http://bugs.python.org/issue670664#msg146770
        
    :copyleft: 2011-2012 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


try:
    import HTMLParser as OriginHTMLParser
except ImportError:
    from html import parser as OriginHTMLParser # python 3


if hasattr(OriginHTMLParser, "cdata_elem"):
    # Current python version is patched -> use the original
    HTMLParser = OriginHTMLParser
else:
    # Current python version is not patched -> use own patched version
    from creole.shared.HTMLParsercompat import HTMLParser
