# -*- coding: utf-8 -*-

"""
    unitest base class
    ~~~~~~~~~~~~~~~~~~

    Basic unittest class for all python-creole tests.

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate:$
    $Rev:$
    $Author$

    :copyleft: 2008-2009 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE.txt for more details.
"""

import sys
import unittest

from utils import MarkupTest

from creole import creole2html, html2creole
from creole.html2creole import HTML_MACRO_UNKNOWN_NODES


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
        self.assertNotEqual(source_string, should_string)

        # prepare whitespace on test strings
        markup_string = self._prepare_text(source_string)
        assert isinstance(markup_string, unicode)

        should = self._prepare_text(should_string)
        assert isinstance(should, unicode)
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

    def assert_html2Creole(self, raw_markup, raw_html, debug=False, **kwargs):
        """
        Compare the genereted markup from the given >raw_html< html code, with
        the given >raw_markup< reference string.
        """
#        assert isinstance(raw_html, unicode)
#        raw_markup = unicode(raw_markup, encoding="utf8")
#        raw_html = unicode(raw_html, "utf8")

        self.assertNotEqual(raw_markup, raw_html)

        # prepare whitespace on test strings
        markup = self._prepare_text(raw_markup)
        assert isinstance(markup, unicode)
        if debug:
            self._debug_text("assert_Creole2html() markup", markup)

        html = self._prepare_text(raw_html)
        assert isinstance(html, unicode)

        # convert html code into creole markup
        out_string = html2creole(html, debug, **kwargs)
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
        source_string = unicode(source_string)
        should_string = unicode(should_string)
        self.assertNotEqual(source_string, should_string)
        self.assert_Creole2html(source_string, should_string, debug)
        self.assert_html2Creole(
            source_string, should_string, debug,
            unknown_emit=HTML_MACRO_UNKNOWN_NODES
        )

