# -*- coding: utf-8 -*-

import sys

from creole_parser import Parser
from creole2html import HtmlEmitter
from html2creole import Html2CreoleParser, Html2CreoleEmitter

# Important for setuptools:
# - Only use . as a separator
# - No spaces: "0.8.0 RC2" -> "0.8.0RC2"
# http://peak.telecommunity.com/DevCenter/setuptools#specifying-your-project-s-version
__version__ = (0, 2, 4, "")
VERSION_STRING = "0.2.4"


def creole2html(markup_string, debug=False, **kwargs):
    """
    convert creole markup into html code

    >>> creole2html(u'This is **creole //markup//**!')
    u'<p>This is <strong>creole <i>markup</i></strong>!</p>\\n'
    """
    # Create document tree from creole markup
    document = Parser(markup_string).parse()
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
    # create the document tree from html code
    h2c = Html2CreoleParser(debug)
    document_tree = h2c.feed(html_string)
    if debug:
        h2c.debug()
   
    # create creole markup from the document tree
    emitter = Html2CreoleEmitter(document_tree, debug=debug, **kwargs)
    return emitter.emit()


if __name__ == '__main__':
    print "runing local doctest..."
    import doctest
    doctest.testmod()#verbose=True)
    print "--END--"