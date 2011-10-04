# coding: utf-8


"""
    Creole macros
    ~~~~~~~~~~~~~
    
    Note: all mecro functions must return unicode!
    
    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

def html(text):
    """
    Macro tag <<html>>...<</html>>
    Pass-trought for html code (or other stuff) 
    """
    return text

