#!/usr/bin/env python
# coding: utf-8

"""
    creole2html unittest
    ~~~~~~~~~~~~~~~~~~~~
    
    Here are only some tests witch doesn't work in the cross compare tests.
    
    Info: There exist some situations with different whitespace handling
        between creol2html and html2creole.

    Test the creole markup.

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE.txt for more details.
"""


import unittest
import StringIO

from tests.utils.base_unittest import BaseCreoleTest

from creole import creole2html


class TestCreole2html(unittest.TestCase):
    """
    Tests around creole2html API and macro function.
    """
    def test_stderr(self):
        """
        Test if the traceback information send to a stderr handler.
        """
        my_stderr = StringIO.StringIO()
        creole2html(
            markup_string=u"<<notexist1>><<notexist2>><</notexist2>>",
            verbose=2, stderr=my_stderr, debug=False
        )
        error_msg = my_stderr.getvalue()

        # Check if we get a traceback information into our stderr handler
        must_have = (
            "<pre>", "</pre>",
            "Traceback",
            "AttributeError:",
            "has no attribute 'notexist1'",
            "has no attribute 'notexist2'",
        )
        for part in must_have:
            self.failUnless(
                part in error_msg,
                "String %r not found in:\n******\n%s******" % (part, error_msg)
            )

    def test_default_macro1(self):
        """
        Test the default "html" macro, found in ./creole/default_macros.py
        """
        html = creole2html(
            markup_string=u"<<html>><p>foo</p><</html>><bar?>",
            verbose=1,
#            stderr=sys.stderr, debug=False
        )
        self.assertEqual(html, u'<p>foo</p>\n<p>&lt;bar?&gt;</p>\n')

    def test_default_macro2(self):
        html = creole2html(
            markup_string=u"<<html>>{{{&lt;nocode&gt;}}}<</html>>",
            verbose=1,
#            stderr=sys.stderr, debug=False
        )
        self.assertEqual(html, u'{{{&lt;nocode&gt;}}}\n')

    def test_default_macro3(self):
        html = creole2html(
            markup_string=u"<<html>>1<</html>><<html>>2<</html>>",
            verbose=1,
#            stderr=sys.stderr, debug=False
        )
        self.assertEqual(html, u'1\n2\n')

    def test_macro_class(self):
        """
        simple test for the "macro API"
        """
        class TestMacro(object):
            def test(self, args, text):
                return u"XXX%s|%sXXX" % (args, text)

        html = creole2html(
            markup_string=u"<<test foo=1>>bar<</test>>",
            macros=TestMacro()
        )
        self.assertEqual(html, u'XXXfoo=1|barXXX\n')

    def test_macro_dict(self):
        """
        simple test for the "macro API"
        """
        def test(args, text):
            return u"XXX%s|%sXXX" % (args, text)

        html = creole2html(
            markup_string=u"<<test foo=1>>bar<</test>>",
            macros={"test": test}
        )
        self.assertEqual(html, u'XXXfoo=1|barXXX\n')

    def test_macro_callable(self):
        """
        simple test for the "macro API"
        """
        def testmacro(macroname, args, text):
            if macroname == "test":
                return u"XXX%s|%sXXX" % (args, text)
            raise AssertionError("Wrong macro name?")

        html = creole2html(
            markup_string=u"<<test foo=1>>bar<</test>>",
            macros=testmacro
        )
        self.assertEqual(html, u'XXXfoo=1|barXXX\n')







class TestCreole2htmlMarkup(BaseCreoleTest):

    def assertCreole(self, *args, **kwargs):
        self.assert_Creole2html(*args, **kwargs)

    #--------------------------------------------------------------------------

    def test_creole_basic(self):
        out_string = creole2html(u"a text line.")
        self.assertEqual(out_string, "<p>a text line.</p>\n")

    def test_lineendings(self):
        """ Test all existing lineending version """
        out_string = creole2html(u"first\nsecond")
        self.assertEqual(out_string, u"<p>first<br />\nsecond</p>\n")

        out_string = creole2html(u"first\rsecond")
        self.assertEqual(out_string, u"<p>first<br />\nsecond</p>\n")

        out_string = creole2html(u"first\r\nsecond")
        self.assertEqual(out_string, u"<p>first<br />\nsecond</p>\n")

    #--------------------------------------------------------------------------

    def test_creole_linebreak(self):
        self.assertCreole(r"""
            Force\\linebreak
        """, """
            <p>Force<br />
            linebreak</p>
        """)

    def test_html_lines(self):
        self.assertCreole(r"""
            This is a normal Text block witch would
            escape html chars like < and > ;)
            
            So you can't insert <html> directly.
            You can use the <<html>><strong>html macro</strong><</html>> for it.
            This is a default macro.
            
            <p>This escaped, too.</p>
        """, """
            <p>This is a normal Text block witch would<br />
            escape html chars like &lt; and &gt; ;)</p>
            
            <p>So you can't insert &lt;html&gt; directly.<br />
            You can use the <strong>html macro</strong> for it.<br />
            This is a default macro.</p>
            
            <p>&lt;p&gt;This escaped, too.&lt;/p&gt;</p>
        """)

    def test_escape_char(self):
        self.assertCreole(r"""
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
        self.assertCreole(r"""
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
        self.assertCreole(r"""
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

        self.assertCreole(r"""
            There exist three different macro types:
            A <<test_macro args="foo1">>bar1<</test_macro>> in a line...
            ...a single <<test_macro args="foo2">> tag,
            or: <<test_macro args="foo2" />> closed...
            
            a macro block:
            <<test_macro args="foo3">>
            the
            text
            <</test_macro>>
            the end
        """, r"""
            <p>There exist three different macro types:<br />
            A [args="foo1" text: bar1] in a line...<br />
            ...a single [args="foo2" text: None] tag,<br />
            or: [args="foo2" text: None] closed...</p>
            
            <p>a macro block:</p>
            [args="foo3" text: the
            text]
            <p>the end</p>
        """)

    def test_macro_html1(self):
        self.assertCreole(r"""
            html macro:
            <<html>>
            <p><<this is broken 'html', but it will be pass throu>></p>
            <</html>>
            
            inline: <<html>>&#x7B;...&#x7D;<</html>> code
        """, r"""
            <p>html macro:</p>
            <p><<this is broken 'html', but it will be pass throu>></p>
            
            <p>inline: &#x7B;...&#x7D; code</p>
        """, #debug=True
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

        self.assertCreole(source_string, should_string, verbose=1)

        #----------------------------------------------------------------------
        # Test with verbose=2 ans a StringIO stderr handler

    def test_macro_not_exist2(self):
        """
        not existing macro with creole2html.HtmlEmitter(verbose=0):
        
        No error messages should be inserted.
        """
        self.assertCreole(r"""
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
        """,
            verbose=0
        )

    def test_image(self):
        """ test image tag with different picture text """
        self.assertCreole(r"""
            {{foobar1.jpg}}
            {{/path1/path2/foobar2.jpg}}
            {{/path1/path2/foobar3.jpg|foobar3.jpg}}
        """, """
            <p><img src="foobar1.jpg" alt="foobar1.jpg" /><br />
            <img src="/path1/path2/foobar2.jpg" alt="/path1/path2/foobar2.jpg" /><br />
            <img src="/path1/path2/foobar3.jpg" alt="foobar3.jpg" /></p>
        """)

    def test_links(self):
        self.assertCreole(r"""
            [[/foobar/Creole_(Markup)]]
            [[http://de.wikipedia.org/wiki/Creole_(Markup)|Creole@wikipedia]]
        """, """
            <p><a href="/foobar/Creole_(Markup)">/foobar/Creole_(Markup)</a><br />
            <a href="http://de.wikipedia.org/wiki/Creole_(Markup)">Creole@wikipedia</a></p>
        """)

    def test_macro_get_raw_content(self):
        """
        A macro should get the complete content without any modifications.
        """
        def testmacro(macroname, args, text):
            self.failUnlessEqual(macroname, "code")
            text = text.replace("{", "&#x7B;").replace("}", "&#x7D;")
            return text

        html = creole2html(
            markup_string=self._prepare_text(u"""
                intro
                <<code>>
                a {{ django }} variable, not a image ;)
                Foo {% blocktag %} bar {% endblocktag %}!
                **bold** //italics//
                <</code>>
                outro
            """),
            macros=testmacro
        )
        self.assertEqual(html, self._prepare_text(u"""
            <p>intro</p>
            a &#x7B;&#x7B; django &#x7D;&#x7D; variable, not a image ;)
            Foo &#x7B;% blocktag %&#x7D; bar &#x7B;% endblocktag %&#x7D;!
            **bold** //italics//
            <p>outro</p>
            
        """))

    def test_wiki_style_line_breaks(self):

        html = creole2html(
            markup_string=self._prepare_text(u"""
                with blog line breaks, every line break would be convertet into <br />
                with wiki style not.
                
                This is the first line,\\\\and this is the second.
                
                new line
                 block 1
                
                new line
                 block 2
                
                end
            """),
            blog_line_breaks=False
        )
        self.assertEqual(html, self._prepare_text(u"""
            <p>with blog line breaks, every line break would be convertet into &lt;br /&gt;with wiki style not.</p>
            
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
        html = creole2html(markup_string=u"== Headline1 == \n== Headline2== ")
        self.assertEqual(html, self._prepare_text(u"""
            <h2>Headline1</h2>
            <h2>Headline2</h2>
            
        """))

    def test_tt(self):
        self.assertCreole(r"""
            inline {{{<escaped>}}} and {{{ **not strong** }}}...
            ...and ##**strong** Teletyper## ;)
        """, """
            <p>inline <tt>&lt;escaped&gt;</tt> and <tt> **not strong** </tt>...<br />
            ...and <tt><strong>strong</strong> Teletyper</tt> ;)</p>
        """)



if __name__ == '__main__':
    unittest.main()
#if __name__ == '__main__':
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreole2html)
#    unittest.TextTestRunner().run(suite)
