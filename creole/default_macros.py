# -*- coding: utf-8 -*-

"""
    Creole macros
    ~~~~~~~~~~~~~
    
    Note: all mecro functions must return unicode!
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
