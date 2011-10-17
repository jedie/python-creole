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

from __future__ import division, absolute_import, print_function, unicode_literals

__version__ = (0, 9, 2)
__api__ = (1, 0) # Creole 1.0 spec - http://wikicreole.org/


import os
import sys

from creole.creole2html.emitter import HtmlEmitter
from creole.creole2html.parser import BlockRules, CreoleParser
from creole.html2creole.emitter import CreoleEmitter
from creole.html2rest.emitter import ReStructuredTextEmitter
from creole.html2textile.emitter import TextileEmitter
from creole.html_parser.parser import HtmlParser
from creole.py3compat import TEXT_TYPE


# TODO: Add git date to __version__


VERSION_STRING = '.'.join(str(part) for part in __version__)
API_STRING = '.'.join(str(integer) for integer in __api__)


def creole2html(markup_string, debug=False, parser_kwargs={}, emitter_kwargs={}):
    """
    convert creole markup into html code

    >>> creole2html('This is **creole //markup//**!')
    '<p>This is <strong>creole <i>markup</i></strong>!</p>'
    """
    assert isinstance(markup_string, TEXT_TYPE), "given markup_string must be unicode!"

    # Create document tree from creole markup
    document = CreoleParser(markup_string, **parser_kwargs).parse()
    if debug:
        document.debug()

    # Build html code from document tree
    #print("creole2html HtmlEmitter kwargs:", emitter_kwargs)
    return HtmlEmitter(document, **emitter_kwargs).emit()


def parse_html(html_string, debug=False, **parser_kwargs):
    """ create the document tree from html code """
    assert isinstance(html_string, TEXT_TYPE), "given html_string must be unicode!"

    h2c = HtmlParser(debug, **parser_kwargs)
    document_tree = h2c.feed(html_string)
    if debug:
        h2c.debug()
    return document_tree


def html2creole(html_string, debug=False, parser_kwargs={}, emitter_kwargs={}):
    """
    convert html code into creole markup

    >>> html2creole('<p>This is <strong>creole <i>markup</i></strong>!</p>')
    'This is **creole //markup//**!'
    """
    document_tree = parse_html(html_string, debug, **parser_kwargs)

    # create creole markup from the document tree
    emitter = CreoleEmitter(document_tree, debug=debug, **emitter_kwargs)
    return emitter.emit()


def html2textile(html_string, debug=False, parser_kwargs={}, emitter_kwargs={}):
    """
    convert html code into textile markup
    
    >>> html2textile('<p>This is <strong>textile <i>markup</i></strong>!</p>')
    'This is *textile __markup__*!'
    """
    document_tree = parse_html(html_string, debug, **parser_kwargs)

    # create creole markup from the document tree
    emitter = TextileEmitter(document_tree, debug=debug, **emitter_kwargs)
    return emitter.emit()


def html2rest(html_string, debug=False, parser_kwargs={}, emitter_kwargs={}):
    """
    convert html code into textile markup
    
    >>> html2rest('<p>This is <strong>ReStructuredText</strong> <em>markup</em>!</p>')
    'This is **ReStructuredText** *markup*!'
    """
    document_tree = parse_html(html_string, debug, **parser_kwargs)

    # create creole markup from the document tree
    emitter = ReStructuredTextEmitter(document_tree, debug=debug, **emitter_kwargs)
    return emitter.emit()



if __name__ == '__main__':
    print("runing local doctest...")
    import doctest
    print(
        doctest.testmod()#verbose=True
    )
