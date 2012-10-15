# coding: utf-8


"""
    unitest base class
    ~~~~~~~~~~~~~~~~~~

    Basic unittest class for all python-creole tests.

    :copyleft: 2008-2009 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import re
import warnings

from creole.tests.utils.utils import MarkupTest
from creole.py3compat import TEXT_TYPE


try:
    import textile
except ImportError:
    test_textile = False
    warnings.warn(
        "Markup error: The Python textile library isn't installed."
        " Download: http://pypi.python.org/pypi/textile"
    )
else:
    test_textile = True


from creole.exceptions import DocutilsImportError
from creole import creole2html, html2creole, html2textile, html2rest

try:
    from creole.rest2html.clean_writer import rest2html
except DocutilsImportError as err:
    REST_INSTALLED = False
    warnings.warn("Can't run all ReSt unittests: %s" % err)
else:
    REST_INSTALLED = True

tabs2spaces_re = re.compile(r"^(\t*)(.*?)$", re.M)



def tabs2spaces(html):
    """ form reformating textile html code
    >>> tabs2spaces("\\t<p>one<br />\\n\\t\\ttwo<br />\\n\\t\\t\\ttree</p>")
    '<p>one<br />\\n  two<br />\\n    tree</p>'
    """
    def reformat_tabs(match):
        tabs = match.group(1)
        text = match.group(2)

        indent = len(tabs) - 1
        if indent < 0:
            indent = 0

#        print(len(tabs), indent, repr(tabs), text)
        return "  " * indent + text
    return tabs2spaces_re.sub(reformat_tabs, html)


def strip_html_lines(html, strip_lines=False):
    """
    >>> strip_html_lines("\t<p>foo   \\n\\n\t\t  bar</p>", strip_lines=True)
    '<p>foo\\nbar</p>'
    """
    html = "\n".join(
        [line.strip(" \t") for line in html.splitlines() if line]
    )
    return html



class BaseCreoleTest(MarkupTest):
    """
    Basic unittest class for all python-creole unittest classes.
    """
    def _debug_text(self, msg, raw_text):
        text = raw_text.replace(" ", ".")
        text = text.replace("\n", "\\n\n")
        text = text.replace("\t", "\\t")

        print
        print("_" * 79)
        print(" Debug Text: %s" % msg)
        print(text)
        print("-" * 79)

    def assertIn(self, member, container, *args, **kwargs):
        """
        Assert member in container.
        assertIn is new in Python 2.7
        """
        try:
            f = super(BaseCreoleTest, self).assertIn
        except AttributeError:
            self.assertTrue(member in container, *args, **kwargs)
        else:
            f(member, container, *args, **kwargs)

    def assert_creole2html(self, raw_creole, raw_html, \
            strip_lines=False, debug=False,
            parser_kwargs={}, emitter_kwargs={},
            block_rules=None, blog_line_breaks=True, macros=None, verbose=None, stderr=None,
        ):
        """
        compare the generated html code from the markup string >creole_string<
        with the >html_string< reference.
        """
        self.assertNotEqual(raw_creole, raw_html)
        self.assertEqual(parser_kwargs, {}, "parser_kwargs is deprecated!")
        self.assertEqual(emitter_kwargs, {}, "parser_kwargs is deprecated!")

        # prepare whitespace on test strings
        markup_string = self._prepare_text(raw_creole)
        assert isinstance(markup_string, TEXT_TYPE)

        html_string = self._prepare_text(raw_html)
        assert isinstance(html_string, TEXT_TYPE)
        if strip_lines:
            html_string = strip_html_lines(html_string, strip_lines)
        if debug:
            self._debug_text("assert_creole2html() html_string", html_string)

        # convert creole markup into html code
        out_string = creole2html(
            markup_string, debug,
            block_rules=block_rules, blog_line_breaks=blog_line_breaks,
            macros=macros, verbose=verbose, stderr=stderr,
        )
        if debug:
            self._debug_text("assert_creole2html() creole2html", out_string)

        if strip_lines:
            out_string = strip_html_lines(out_string, strip_lines)
        else:
            out_string = out_string.replace("\t", "    ")

        # compare
        self.assertEqual(out_string, html_string, msg="creole2html")

    def assert_html2creole2(self, creole, html, debug=False, unknown_emit=None):
        # convert html code into creole markup
        out_string = html2creole(html, debug, unknown_emit=unknown_emit)
        if debug:
            self._debug_text("assert_html2creole() html2creole", out_string)

        # compare
        self.assertEqual(out_string, creole, msg="html2creole")

    def assert_html2creole(self, raw_creole, raw_html, \
                strip_lines=False, debug=False,
                # OLD API:
                parser_kwargs={}, emitter_kwargs={},
                # html2creole:
                unknown_emit=None
        ):
        """
        Compare the genereted markup from the given >raw_html< html code, with
        the given >creole_string< reference string.
        """
        self.assertEqual(parser_kwargs, {}, "parser_kwargs is deprecated!")
        self.assertEqual(emitter_kwargs, {}, "parser_kwargs is deprecated!")
#        assert isinstance(raw_html, TEXT_TYPE)
#        creole_string = unicode(creole_string, encoding="utf8")
#        raw_html = unicode(raw_html, "utf8")

        self.assertNotEqual(raw_creole, raw_html)

        # prepare whitespace on test strings
        creole = self._prepare_text(raw_creole)
        assert isinstance(creole, TEXT_TYPE)
        if debug:
            self._debug_text("assert_creole2html() markup", creole)

        html = self._prepare_text(raw_html)
        assert isinstance(html, TEXT_TYPE)

        self.assert_html2creole2(creole, html, debug, unknown_emit)


    def cross_compare_creole(self, creole_string, html_string,
                        strip_lines=False, debug=False,
                        # creole2html old API:
                        creole_parser_kwargs={}, html_emitter_kwargs={},
                        # html2creole old API:
                        html_parser_kwargs={}, creole_emitter_kwargs={},

                        # creole2html new API:
                        block_rules=None, blog_line_breaks=True, macros=None, stderr=None,
                        # html2creole:
                        unknown_emit=None
        ):
        """
        Cross compare with:
            * creole2html
            * html2creole
        """
        self.assertEqual(creole_parser_kwargs, {}, "creole_parser_kwargs is deprecated!")
        self.assertEqual(html_emitter_kwargs, {}, "html_emitter_kwargs is deprecated!")
        self.assertEqual(html_parser_kwargs, {}, "html_parser_kwargs is deprecated!")
        self.assertEqual(creole_emitter_kwargs, {}, "creole_emitter_kwargs is deprecated!")

        assert isinstance(creole_string, TEXT_TYPE)
        assert isinstance(html_string, TEXT_TYPE)
        self.assertNotEqual(creole_string, html_string)

        self.assert_creole2html(
            creole_string, html_string, strip_lines, debug,
            block_rules=block_rules, blog_line_breaks=blog_line_breaks,
            macros=macros, stderr=stderr,
        )

        self.assert_html2creole(
            creole_string, html_string, strip_lines, debug,
            unknown_emit=unknown_emit,
        )

    def assert_html2textile(self, textile_string, html_string, \
                        strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
        """
        Check html2textile
        """
        self.assertNotEqual(textile_string, html_string)

        textile_string = self._prepare_text(textile_string)
        html_string = self._prepare_text(html_string)

        if strip_lines:
            html_string = strip_html_lines(html_string, strip_lines)

        # compare html -> textile
        textile_string2 = html2textile(html_string, debug, parser_kwargs, emitter_kwargs)
        if debug:
            print("-" * 79)
            print(textile_string2)
            print("-" * 79)

        self.assertEqual(textile_string2, textile_string, msg="html2textile")

        return textile_string, html_string

    def cross_compare_textile(self, textile_string, html_string, \
                        strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
        """
            Checks:
                * html2textile
                * textile2html
        """
#        assert isinstance(textile_string, TEXT_TYPE)
#        assert isinstance(html_string, TEXT_TYPE)
        self.assertNotEqual(textile_string, html_string)

        # compare html -> textile
        textile_string, html_string = self.assert_html2textile(
            textile_string, html_string,
            strip_lines, debug, parser_kwargs, emitter_kwargs
        )

        # compare textile -> html
        if not test_textile:
            warnings.warn("Skip textile test. Please install python textile module.")
            return

        html = textile.textile(textile_string)
        html = html.replace("<br />", "<br />\n")
        html = tabs2spaces(html)
        if strip_lines:
            html = strip_html_lines(html, strip_lines)

        self.assertEqual(html_string, html, msg="textile2html")

    def assert_html2rest(self, rest_string, html_string, \
                        strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
        """
        Check html to reStructuredText converter
        """
        self.assertNotEqual(rest_string, html_string)

        rest_string = self._prepare_text(rest_string)
        html_string = self._prepare_text(html_string)

        if strip_lines:
            html_string = strip_html_lines(html_string, strip_lines)

        # compare html -> reStructuredText
        rest_string2 = html2rest(html_string, debug, parser_kwargs, emitter_kwargs)
        if debug:
            print("-" * 79)
            print(rest_string2)
            print("-" * 79)

        self.assertEqual(rest_string2, rest_string, msg="html2rest")

        return rest_string, html_string

    def assert_rest2html(self, rest_string, html_string, \
            strip_lines=False, debug=False, prepare_strings=True, **kwargs):

        # compare rest -> html
        if not REST_INSTALLED:
            warnings.warn("Skip ReSt test. Please install Docutils.")
            return

        if prepare_strings:
            rest_string = self._prepare_text(rest_string)
            html_string = self._prepare_text(html_string)

        html = rest2html(rest_string, **kwargs)

        if debug:
            print(rest_string)
            print(html_string)
            print(html)

        html = html.strip()
#        html = html.replace("<br />", "<br />\n")
#        html = tabs2spaces(html)
        if strip_lines:
            html = strip_html_lines(html, strip_lines)

        self.assertEqual(html, html_string, msg="rest2html")

    def cross_compare_rest(self, rest_string, html_string, \
                        strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
#        assert isinstance(textile_string, TEXT_TYPE)
#        assert isinstance(html_string, TEXT_TYPE)
        self.assertNotEqual(rest_string, html_string)

        rest_string, html_string = self.assert_html2rest(
            rest_string, html_string,
            strip_lines, debug, parser_kwargs, emitter_kwargs
        )

        # compare rest -> html
        self.assert_rest2html(
            rest_string, html_string,
            strip_lines=strip_lines, debug=debug,
            prepare_strings=False,
        )

    def cross_compare(self,
            html_string,
            creole_string=None,
            textile_string=None,
            rest_string=None,
            strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
        """
        Cross compare with:
            * creole2html
            * html2creole
            * html2textile
            * html2ReSt
        """
        if creole_string:
            self.cross_compare_creole(
                creole_string, html_string, strip_lines, debug, parser_kwargs, emitter_kwargs
            )

        if textile_string:
            self.cross_compare_textile(
                textile_string, html_string, strip_lines, debug, parser_kwargs, emitter_kwargs
            )

        if rest_string:
            self.cross_compare_rest(
                rest_string, html_string, strip_lines, debug, parser_kwargs, emitter_kwargs
            )

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
