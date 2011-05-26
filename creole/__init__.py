# coding: utf-8


"""
    python-creole
    ~~~~~~~~~~~~~

    :homepage:
      http://code.google.com/p/python-creole/
    
    :sourcecode:
      http://github.com/jedie/python-creole
    
    :PyPi:
      http://pypi.python.org/pypi/python-creole/

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


__version__ = (0, 5, 0, "pre")
__api__ = (1, 0) # Creole 1.0 spec - http://wikicreole.org/


import os
import sys


from creole.creole2html.parser import BlockRules, CreoleParser
from creole.creole2html.emitter import HtmlEmitter
from creole.html2creole.parser import HtmlParser
from creole.html2creole.emitter import CreoleEmitter


# TODO: Add git date to __version__


VERSION_STRING = '.'.join(str(part) for part in __version__)
API_STRING = '.'.join(str(integer) for integer in __api__)


def creole2html(markup_string, debug=False, blog_line_breaks=True, **kwargs):
    """
    convert creole markup into html code

    >>> creole2html(u'This is **creole //markup//**!')
    u'<p>This is <strong>creole <i>markup</i></strong>!</p>\\n'
    """
    assert isinstance(markup_string, unicode)

    # Create document tree from creole markup
    document = CreoleParser(markup_string, BlockRules(blog_line_breaks)).parse()
    if debug:
        document.debug()

    # Build html code from document tree
    return HtmlEmitter(document, **kwargs).emit()



def html2creole(html_string, debug=False, **kwargs):
    """
    convert html code into creole markup

    >>> html2creole(u'<p>This is <strong>creole <i>markup</i></strong>!</p>')
    u'This is **creole //markup//**!'
    """
    assert isinstance(html_string, unicode)

    # create the document tree from html code
    h2c = HtmlParser(debug)
    document_tree = h2c.feed(html_string)
    if debug:
        h2c.debug()

    # create creole markup from the document tree
    emitter = CreoleEmitter(document_tree, debug=debug, **kwargs)
    return emitter.emit()


if __name__ == '__main__':
    print "runing local doctest..."
    import doctest
    print doctest.testmod()#verbose=True)
