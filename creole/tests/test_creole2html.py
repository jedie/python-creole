#!/usr/bin/env python
# coding: utf-8

"""
    creole2html unittest
    ~~~~~~~~~~~~~~~~~~~~
    
    Here are only some tests witch doesn't work in the cross compare tests.
    
    Info: There exist some situations with different whitespace handling
        between creol2html and html2creole.

    Test the creole markup.

    :copyleft: 2008-2012 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import sys
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO # python 3

from creole.tests.utils.base_unittest import BaseCreoleTest
from creole.tests import test_macros

from creole import creole2html
from creole.shared import example_macros
from creole.shared.utils import string2dict, dict2string


class TestCreole2html(unittest.TestCase):
    """
    Tests around creole2html API and macro function.
    """
    def assertIn(self, src, dst):
        # assertIn is new in Python 2.7 ;)
        self.assertFalse(src not in dst, "%r not found in %r" % (src, dst))

    def test_stderr(self):
        """
        Test if the traceback information send to a stderr handler.
        """
        my_stderr = StringIO()
        creole2html(
            markup_string="<<notexist1>><<notexist2>><</notexist2>>",
            emitter_kwargs={
                "verbose":2,
                "stderr":my_stderr,
            }
        )
        error_msg = my_stderr.getvalue()

        # Check if we get a traceback information into our stderr handler
        must_have = (
            "Traceback",
            "AttributeError:",
            "has no attribute 'notexist1'",
            "has no attribute 'notexist2'",
        )

        for part in must_have:
            self.assertIn(part, error_msg)

    def test_example_macros1(self):
        """
        Test the default "html" macro, found in ./creole/default_macros.py
        """
        html = creole2html(
            markup_string="<<html>><p>foo</p><</html>><bar?>",
            emitter_kwargs={
                "verbose":1,
                "macros":example_macros,
                "stderr":sys.stderr,
            }
        )
        self.assertEqual(html, '<p>foo</p>\n<p>&lt;bar?&gt;</p>')

    def test_example_macros2(self):
        html = creole2html(
            markup_string="<<html>>{{{&lt;nocode&gt;}}}<</html>>",
            emitter_kwargs={
                "verbose":1,
                "macros":example_macros,
                "stderr":sys.stderr,
            }
        )
        self.assertEqual(html, '{{{&lt;nocode&gt;}}}')

    def test_example_macros3(self):
        html = creole2html(
            markup_string="<<html>>1<</html>><<html>>2<</html>>",
            emitter_kwargs={
                "verbose":1,
                "macros":example_macros,
                "stderr":sys.stderr,
            }
        )
        self.assertEqual(html, '1\n2')

    def test_macro_dict(self):
        """
        simple test for the "macro API"
        """
        def test(text, foo, bar):
            return "|".join([foo, bar, text])

        html = creole2html(
            markup_string="<<test bar='b' foo='a'>>c<</test>>",
            emitter_kwargs={
                "verbose":1,
                "macros":{"test":test},
                "stderr":sys.stderr,
            }
        )
        self.assertEqual(html, 'a|b|c')

    def test_macro_callable(self):
        """
        simple test for the "macro API"
        """
        def testmacro():
            pass

        self.assertRaises(DeprecationWarning,
            creole2html,
            markup_string="<<test no=1 arg2='foo'>>bar<</test>>",
            emitter_kwargs={
                "verbose":1,
                "macros":testmacro,
                "stderr":sys.stderr,
            }
        )

    def test_macro_wrong_arguments_with_error_report(self):
        """
        simple test for the "macro API"
        """
        def test(text, foo):
            pass
        my_stderr = StringIO()

        html = creole2html(
            markup_string="<<test bar='foo'>>c<</test>>",
            emitter_kwargs={
                "verbose":2,
                "macros":{"test":test},
                "stderr":my_stderr,
            }
        )
        self.assertEqual(html,
            "[Error: Macro 'test' error: test() got an unexpected keyword argument 'bar']"
        )
        error_msg = my_stderr.getvalue()

        # Check traceback information into our stderr handler
        must_have = (
            "TypeError: test() got an unexpected keyword argument 'bar'",
            "sourceline: 'def test(text, foo):' from",
            "tests/test_creole2html.py",
        )
        for part in must_have:
            self.assertIn(part, error_msg)


    def test_macro_wrong_arguments_quite(self):
        """
        simple test for the "macro API"
        """
        def test(text, foo):
            pass
        my_stderr = StringIO()

        html = creole2html(
            markup_string="<<test bar='foo'>>c<</test>>",
            emitter_kwargs={
                "verbose":1,
                "macros":{"test":test},
                "stderr":my_stderr,
            }
        )
        self.assertEqual(html,
            "[Error: Macro 'test' error: test() got an unexpected keyword argument 'bar']"
        )
        error_msg = my_stderr.getvalue()
        self.assertEqual(error_msg, "")






class TestCreole2htmlMarkup(BaseCreoleTest):

    def test_creole_basic(self):
        out_string = creole2html("a text line.")
        self.assertEqual(out_string, "<p>a text line.</p>")

    def test_lineendings(self):
        """ Test all existing lineending version """
        out_string = creole2html("first\nsecond")
        self.assertEqual(out_string, "<p>first<br />\nsecond</p>")

        out_string = creole2html("first\rsecond")
        self.assertEqual(out_string, "<p>first<br />\nsecond</p>")

        out_string = creole2html("first\r\nsecond")
        self.assertEqual(out_string, "<p>first<br />\nsecond</p>")

    #--------------------------------------------------------------------------

    def test_creole_linebreak(self):
        self.assert_creole2html(r"""
            Force\\linebreak
        """, """
            <p>Force<br />
            linebreak</p>
        """)

    def test_html_lines(self):
        self.assert_creole2html(r"""
            This is a normal Text block witch would
            escape html chars like < and > ;)
            
            So you can't insert <html> directly.
            
            <p>This escaped, too.</p>
        """, """
            <p>This is a normal Text block witch would<br />
            escape html chars like &lt; and &gt; ;)</p>
            
            <p>So you can't insert &lt;html&gt; directly.</p>
            
            <p>&lt;p&gt;This escaped, too.&lt;/p&gt;</p>
        """)

    def test_escape_char(self):
        self.assert_creole2html(r"""
            ~#1
            http://domain.tld/~bar/
            ~http://domain.tld/
            [[Link]]
            ~[[Link]]
        """, """
            <p>#1<br />
            <a href="http://domain.tld/~bar/">http://domain.tld/~bar/</a><br />
            http://domain.tld/<br />
            <a href="Link">Link</a><br />
            [[Link]]</p>
        """)

    def test_cross_paragraphs(self):
        self.assert_creole2html(r"""
            Bold and italics should //not be...

            ...able// to **cross 
            
            paragraphs.**
        """, """
            <p>Bold and italics should //not be...</p>
            
            <p>...able// to **cross</p>
            
            <p>paragraphs.**</p>
        """)

    def test_list_special(self):
        """
        optional whitespace before the list 
        """
        self.assert_creole2html(r"""
            * Item 1
            ** Item 1.1
             ** Item 1.2
                ** Item 1.3
                    * Item2
            
                # one
              ## two
        """, """
        <ul>
            <li>Item 1
            <ul>
                <li>Item 1.1</li>
                <li>Item 1.2</li>
                <li>Item 1.3</li>
            </ul></li>
            <li>Item2</li>
        </ul>
        <ol>
            <li>one
            <ol>
                <li>two</li>
            </ol></li>
        </ol>
        """)

    def test_macro_basic(self):
        """
        Test the three diferent macro types with a "unittest macro"
        """
        self.assert_creole2html(r"""
            There exist three different macro types:
            A <<test_macro1 args="foo1">>bar1<</test_macro1>> in a line...
            ...a single <<test_macro1 foo="bar">> tag,
            or: <<test_macro1 a=1 b=2 />> closed...
            
            a macro block:
            <<test_macro2 char="|">>
            the
            text
            <</test_macro2>>
            the end
        """, r"""
            <p>There exist three different macro types:<br />
            A [test macro1 - kwargs: args='foo1',text='bar1'] in a line...<br />
            ...a single [test macro1 - kwargs: foo='bar',text=None] tag,<br />
            or: [test macro1 - kwargs: a=1,b=2,text=None] closed...</p>
            
            <p>a macro block:</p>
            the|text
            <p>the end</p>
        """,
            macros=test_macros,
        )

    def test_macro_html1(self):
        self.assert_creole2html(r"""
                html macro:
                <<html>>
                <p><<this is broken 'html', but it will be pass throu>></p>
                <</html>>
                
                inline: <<html>>&#x7B;...&#x7D;<</html>> code
            """, r"""
                <p>html macro:</p>
                <p><<this is broken 'html', but it will be pass throu>></p>
                
                <p>inline: &#x7B;...&#x7D; code</p>
            """,
            macros=example_macros,
        )

    def test_macro_not_exist1(self):
        """
        not existing macro with creole2html.HtmlEmitter(verbose=1):
        A error message should be insertet into the generated code
        
        Two tests: with verbose=1 and verbose=2, witch write a Traceback
        information to a given "stderr"
        """
        source_string = r"""
            macro block:
            <<notexists>>
            foo bar
            <</notexists>>
            
            inline macro:
            <<notexisttoo foo="bar">>
        """
        should_string = r"""
            <p>macro block:</p>
            [Error: Macro 'notexists' doesn't exist]
            
            <p>inline macro:<br />
            [Error: Macro 'notexisttoo' doesn't exist]
            </p>
        """

        self.assert_creole2html(source_string, should_string, verbose=1)

        #----------------------------------------------------------------------
        # Test with verbose=2 ans a StringIO stderr handler

    def test_wrong_macro_syntax(self):
        self.assert_creole2html(r"""
                wrong macro line:
                <<summary>Some funky page summary.<</summary>>
            """, r"""
                <p>wrong macro line:<br />
                [Error: Wrong macro arguments: '>Some funky page summary.<</summary' for macro 'summary' (maybe wrong macro tag syntax?)]
                </p>
            """, #verbose=True
        )

    def test_macro_not_exist2(self):
        """
        not existing macro with creole2html.HtmlEmitter(verbose=0):
        
        No error messages should be inserted.
        """
        self.assert_creole2html(r"""
            macro block:
            <<notexists>>
            foo bar
            <</notexists>>
            
            inline macro:
            <<notexisttoo foo="bar">>
        """, r"""
            <p>macro block:</p>
            
            <p>inline macro:<br />
            </p>
        """, verbose=False
        )

    def test_image(self):
        """ test image tag with different picture text """
        self.assert_creole2html(r"""
            {{foobar1.jpg}}
            {{/path1/path2/foobar2.jpg}}
            {{/path1/path2/foobar3.jpg|foobar3.jpg}}
        """, """
            <p><img src="foobar1.jpg" title="foobar1.jpg" alt="foobar1.jpg" /><br />
            <img src="/path1/path2/foobar2.jpg" title="/path1/path2/foobar2.jpg" alt="/path1/path2/foobar2.jpg" /><br />
            <img src="/path1/path2/foobar3.jpg" title="foobar3.jpg" alt="foobar3.jpg" /></p>
        """)

    def test_image_unknown_extension(self):
        self.assert_creole2html(r"""
            # {{/path/to/image.ext|image ext}} one
            # {{/no/extension|no extension}} two
            # {{/image.xyz}} tree
        """, """
            <ol>
                <li><img src="/path/to/image.ext" title="image ext" alt="image ext" /> one</li>
                <li><img src="/no/extension" title="no extension" alt="no extension" /> two</li>
                <li><img src="/image.xyz" title="/image.xyz" alt="/image.xyz" /> tree</li>
            </ol>
        """)

    def test_links(self):
        self.assert_creole2html(r"""
            [[/foobar/Creole_(Markup)]]
            [[http://de.wikipedia.org/wiki/Creole_(Markup)|Creole@wikipedia]]
        """, """
            <p><a href="/foobar/Creole_(Markup)">/foobar/Creole_(Markup)</a><br />
            <a href="http://de.wikipedia.org/wiki/Creole_(Markup)">Creole@wikipedia</a></p>
        """)

    def test_standalone_hyperlink(self):
        self.assert_creole2html(r"""
                a link to the http://www.pylucid.org page. 
            """, """
                <p>a link to the <a href="http://www.pylucid.org">http://www.pylucid.org</a> page.</p>
            """
        )

    def test_wiki_style_line_breaks1(self):
        html = creole2html(
            markup_string=self._prepare_text("""
                wiki style
                linebreaks
                
                ...and not blog styled.
            """),
            parser_kwargs={"blog_line_breaks":False},
        )
        self.assertEqual(html, self._prepare_text("""
            <p>wiki style linebreaks</p>
            
            <p>...and not blog styled.</p>
        """))

    def test_wiki_style_line_breaks2(self):
        html = creole2html(
            markup_string=self._prepare_text("""
                **one**
                //two//
                
                * one
                * two
            """),
            parser_kwargs={"blog_line_breaks":False},
        )
        self.assertEqual(html, self._prepare_text("""
            <p><strong>one</strong> <i>two</i></p>
            
            <ul>
            \t<li>one</li>
            \t<li>two</li>
            </ul>
        """))

    def test_wiki_style_line_breaks3(self):
        html = creole2html(
            markup_string=self._prepare_text("""
                with blog line breaks, every line break would be convertet into<br />
                with wiki style not.
                
                This is the first line,\\\\and this is the second.
                
                new line
                block 1
                
                new line
                block 2
                
                end
            """),
            parser_kwargs={"blog_line_breaks":False},
        )
        self.assertEqual(html, self._prepare_text("""
            <p>with blog line breaks, every line break would be convertet into&lt;br /&gt; with wiki style not.</p>
            
            <p>This is the first line,<br />
            and this is the second.</p>
            
            <p>new line block 1</p>
            
            <p>new line block 2</p>
            
            <p>end</p>
        """))


    def test_headline_spaces(self):
        """
        https://code.google.com/p/python-creole/issues/detail?id=15
        """
        html = creole2html(markup_string="== Headline1 == \n== Headline2== ")
        self.assertEqual(html, self._prepare_text("""
            <h2>Headline1</h2>
            <h2>Headline2</h2>
        """))

    def test_tt(self):
        self.assert_creole2html(r"""
            inline {{{<escaped>}}} and {{{ **not strong** }}}...
            ...and ##**strong** Teletyper## ;)
        """, """
            <p>inline <tt>&lt;escaped&gt;</tt> and <tt> **not strong** </tt>...<br />
            ...and <tt><strong>strong</strong> Teletyper</tt> ;)</p>
        """)

    def test_protocol_in_brackets(self):
        self.assert_creole2html(r"""
            My Server ([[ftp://foo/bar]]) is ok.
        """, """
            <p>My Server (<a href="ftp://foo/bar">ftp://foo/bar</a>) is ok.</p>
        """)
        self.assert_creole2html(r"""
            My Server (ftp://foo/bar) is ok.
        """, """
            <p>My Server (ftp://foo/bar) is ok.</p>
        """)

    def test_protocol_with_brackets(self):
        self.assert_creole2html(r"""
            A http://en.wikipedia.org/wiki/Uri_(Island) link.
        """, """
            <p>A <a href="http://en.wikipedia.org/wiki/Uri_(Island)">http://en.wikipedia.org/wiki/Uri_(Island)</a> link.</p>
        """)

    def test_wrong_protocol(self):
        self.assert_creole2html(r"""
            ~ftp://ok
        """, """
            <p>ftp://ok</p>
        """)
        self.assert_creole2html(r"""
            ftp:
        """, """
            <p>ftp:</p>
        """)
        self.assert_creole2html(r"""
            ftp:/
        """, """
            <p>ftp:/</p>
        """)
        self.assert_creole2html(r"""
            missing space.ftp://ok
        """, """
            <p>missing space.ftp://ok</p>
        """)


class TestStr2Dict(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            string2dict('key1="value1" key2="value2"'),
            {'key2': 'value2', 'key1': 'value1'}
        )

    def test_bool(self):
        self.assertEqual(
            string2dict('unicode=True'),
            {'unicode': True}
        )

    def test_mixed1(self):
        self.assertEqual(
            string2dict('A="B" C=1 D=1.1 E=True F=False G=None'),
            {'A': 'B', 'C': 1, 'E': True, 'D': '1.1', 'G': None, 'F': False}
        )

    def test_mixed2(self):
        self.assertEqual(
            string2dict('''key1="'1'" key2='"2"' key3="""'3'""" '''),
            {'key3': 3, 'key2': 2, 'key1': 1}
        )

class TestDict2String(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            dict2string({'key':'value'}),
            "key='value'"
        )

    def test_basic2(self):
        self.assertEqual(
            dict2string({'foo':"bar", "no":123}),
            "foo='bar' no=123"
        )
    def test_basic3(self):
        self.assertEqual(
            dict2string({"foo":'bar', "no":"ABC"}),
            "foo='bar' no='ABC'"
        )

if __name__ == '__main__':
    unittest.main(
        verbosity=2
    )
