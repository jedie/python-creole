# -*- coding: utf-8 -*-

"""
    unitest base class
    ~~~~~~~~~~~~~~~~~~
    
    Basic unittest class for all python-creole tests.
   
    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate:$
    $Rev:$
    $Author: JensDiemer $

    :copyleft: 2008-2009 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE.txt for more details.
"""

import sys
import unittest

from utils import MarkupTest

from creole import creole2html, html2creole


class BaseCreoleTest(MarkupTest):
    """
    Basic unittest class for all python-creole unittest classes.
    """
    def _debug_text(self, msg, raw_text):
        text = raw_text.replace(" ", ".")
        text = text.replace("\n", "\\n\n")
        text = text.replace("\t", "\\t")
        
        print
        print "_"*79
        print " Debug Text: %s" % msg
        print text
        print "-"*79
        
    def assert_Creole2html(self, source_string, should_string, \
                                    verbose=1, stderr=sys.stderr, debug=False):
        """
        compare the generated html code from the markup string >source_string<
        with the >should_string< reference.
        """
        # prepare whitespace on test strings
        markup_string = self._prepare_text(source_string)
        
        should = self._prepare_text(should_string)
        if debug:
            self._debug_text("assert_Creole2html() should_string", should)
        
        # convert creole markup into html code
        out_string = creole2html(
            markup_string, verbose=verbose, stderr=stderr, debug=debug
        )
        if debug:
            self._debug_text("assert_Creole2html() creole2html", out_string)
        
        out_string = out_string.rstrip("\n")
        out_string = out_string.replace("\t", "    ")
        
        # compare
        self.assertEqual(out_string, should)
        
    def assert_html2Creole(self, raw_markup, raw_html, debug=False):
        """
        Compare the genereted markup from the given >raw_html< html code, with
        the given >raw_markup< reference string.
        """
        # prepare whitespace on test strings
        markup = self._prepare_text(raw_markup)
        if debug:
            self._debug_text("assert_Creole2html() markup", markup)
        
        html = self._prepare_text(raw_html)
        
        # convert html code into creole markup
        out_string = html2creole(html, debug)
        if debug:
            self._debug_text("assert_html2Creole() html2creole", out_string)
        
        # compare
        self.assertEqual(out_string, markup)

    def assertCreole(self, source_string, should_string, debug=False):
        """
        Cross compare with creol2html _and_ html2creole with the same given
        refenrece strings.
        
        This only works fine if there is no problematic whitespace handling.
        """
        self.assert_Creole2html(source_string, should_string, debug)
        self.assert_html2Creole(source_string, should_string, debug)

    
#    def _parse(self, txt):
#        """
#        Apply creole markup on txt
#        """
#        document = Parser(txt).parse()
#        out_string = HtmlEmitter(document, verbose=1).emit()
#        #print ">>>%r<<<" % out_string
#        return out_string
#
#    def _processCreole(self, source_string, should_string):
#        """
#        prepate the given text and apply the markup.
#        """
#        source = self._prepare_text(source_string)
#        should = self._prepare_text(should_string)
#        out_string = self._parse(source)
#        return out_string, should
#
#    def assertCreole(self, source_string, should_string):
#        """
#        applies the tinyTextile markup to the given source_string and compairs
#        it with the should_string.
#        """
#        out_string, should = self._processCreole(
#            source_string, should_string
#        )
#        out_string = out_string.rstrip("\n")
#        self.assertEqual(out_string, should)

    #--------------------------------------------------------------------------