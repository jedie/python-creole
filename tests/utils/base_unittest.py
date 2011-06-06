# coding: utf-8


"""
    unitest base class
    ~~~~~~~~~~~~~~~~~~

    Basic unittest class for all python-creole tests.

    :copyleft: 2008-2009 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import re
import warnings

try:
    import textile
except ImportError:
    textile = False
    warnings.warn(
        "Markup error: The Python textile library isn't installed."
        " Download: http://cheeseshop.python.org/pypi/textile"
    )

from utils import MarkupTest

from creole import creole2html, html2creole, html2textile


tabs2spaces_re = re.compile(r"^(\t*)(.*?)$", re.M)

def tabs2spaces(html):
    """ form reformating textile html code
    >>> tabs2spaces(u"\\t<p>one<br />\\n\\t\\ttwo<br />\\n\\t\\t\\ttree</p>")
    u'<p>one<br />\\n  two<br />\\n    tree</p>'
    """
    def reformat_tabs(match):
        tabs = match.group(1)
        text = match.group(2)

        indent = len(tabs) - 1
        if indent < 0:
            indent = 0

#        print len(tabs), indent, repr(tabs), text
        return u"  " * indent + text
    return tabs2spaces_re.sub(reformat_tabs, html)


def strip_html_lines(html, strip_lines=False):
    """
    >>> strip_html_lines(u"\t<p>foo   \\n\\n\t\t  bar</p>", strip_lines=True)
    u'<p>foo\\nbar</p>'
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
        print "_" * 79
        print " Debug Text: %s" % msg
        print text
        print "-" * 79

    def assert_creole2html(self, raw_creole, raw_html, \
            strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
        """
        compare the generated html code from the markup string >creole_string<
        with the >html_string< reference.
        """
        self.assertNotEqual(raw_creole, raw_html)

        # prepare whitespace on test strings
        markup_string = self._prepare_text(raw_creole)
        assert isinstance(markup_string, unicode)

        html_string = self._prepare_text(raw_html)
        assert isinstance(html_string, unicode)
        if strip_lines:
            html_string = strip_html_lines(html_string, strip_lines)
        if debug:
            self._debug_text("assert_creole2html() html_string", html_string)

        # convert creole markup into html code
        out_string = creole2html(
            markup_string, debug, parser_kwargs, emitter_kwargs
        )
        if debug:
            self._debug_text("assert_creole2html() creole2html", out_string)

        if strip_lines:
            out_string = strip_html_lines(out_string, strip_lines)
        else:
            out_string = out_string.replace("\t", "    ")

        # compare
        try:
            self.assertEqual(out_string, html_string)
        except:
            print " *** Error in creole2html:"
            raise

    def assert_html2creole(self, raw_creole, raw_html, \
                strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
        """
        Compare the genereted markup from the given >raw_html< html code, with
        the given >creole_string< reference string.
        """
#        assert isinstance(raw_html, unicode)
#        creole_string = unicode(creole_string, encoding="utf8")
#        raw_html = unicode(raw_html, "utf8")

        self.assertNotEqual(raw_creole, raw_html)

        # prepare whitespace on test strings
        markup = self._prepare_text(raw_creole)
        assert isinstance(markup, unicode)
        if debug:
            self._debug_text("assert_creole2html() markup", markup)

        html = self._prepare_text(raw_html)
        assert isinstance(html, unicode)

        # convert html code into creole markup
        out_string = html2creole(html, debug, parser_kwargs, emitter_kwargs)
        if debug:
            self._debug_text("assert_html2creole() html2creole", out_string)

        # compare
        try:
            self.assertEqual(out_string, markup)
        except:
            print " *** Error in html2creole:"
            raise

    def cross_compare_creole(self, creole_string, html_string,
                        strip_lines=False, debug=False,
                        # creole2html:
                        creole_parser_kwargs={}, html_emitter_kwargs={},
                        # html2creole:
                        html_parser_kwargs={}, creole_emitter_kwargs={},
                                                                            ):
        """
        Cross compare with:
            * creole2html
            * html2creole
        """
        creole_string = unicode(creole_string)
        html_string = unicode(html_string)
        self.assertNotEqual(creole_string, html_string)

        self.assert_creole2html(
            creole_string, html_string, strip_lines, debug,
            creole_parser_kwargs, html_emitter_kwargs
        )

        self.assert_html2creole(
            creole_string, html_string, strip_lines, debug,
            html_parser_kwargs, creole_emitter_kwargs
        )

    def assert_html2textile(self, textile_string, html_string, \
                        strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
        self.assertNotEqual(textile_string, html_string)

        textile_string = self._prepare_text(textile_string)
        html_string = self._prepare_text(html_string)

        if strip_lines:
            html_string = strip_html_lines(html_string, strip_lines)

        # compare html -> textile
        textile_string2 = html2textile(html_string, debug, parser_kwargs, emitter_kwargs)
        if debug:
            print "-" * 79
            print textile_string2
            print "-" * 79

        try:
            self.assertEqual(textile_string2, textile_string)
        except:
            print " *** Error in html2textile:"
            raise

        return textile_string, html_string

    def cross_compare_textile(self, textile_string, html_string, \
                        strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
#        assert isinstance(textile_string, unicode)
#        assert isinstance(html_string, unicode)
        self.assertNotEqual(textile_string, html_string)

        textile_string, html_string = self.assert_html2textile(
            textile_string, html_string,
            strip_lines, debug, parser_kwargs, emitter_kwargs
        )

        # compare textile -> html
        if not textile:
            warnings.warn("Skip textile test. Please install python textile module.")
        else:
            html = textile.textile(textile_string)
            html = html.replace("<br />", "<br />\n")
            html = tabs2spaces(html)
            if strip_lines:
                html = strip_html_lines(html, strip_lines)
            try:
                self.assertEqual(html_string, html)
            except:
                print " *** Error in compare textile -> html:"
                raise

    def cross_compare(self, creole_string, textile_string, html_string, \
            strip_lines=False, debug=False, parser_kwargs={}, emitter_kwargs={}):
        """
        Cross compare with:
            * creole2html
            * html2creole
            * html2textile

        This only works fine if there is no problematic whitespace handling.
        """
        self.cross_compare_creole(
            creole_string, html_string, strip_lines, debug, parser_kwargs, emitter_kwargs
        )

        self.cross_compare_textile(
            textile_string, html_string, strip_lines, debug, parser_kwargs, emitter_kwargs
        )

if __name__ == '__main__':
    import doctest
    print doctest.testmod()
