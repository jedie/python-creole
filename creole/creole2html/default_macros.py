# coding: utf-8


"""
    Creole macros
    ~~~~~~~~~~~~~
    
    Note: all mecro functions must return unicode!
    
    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


def html(args, text):
    """
    Macro tag <<html>>...<</html>>
    Pass-trought for html code (or other stuff) 
    """
    return text


def test_macro(args, text):
    """
    a macro only for testing
    """
    return u"[%s text: %s]" % (args, text)
