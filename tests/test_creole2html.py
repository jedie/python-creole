#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    creole2html unittest
    ~~~~~~~~~~~~~~~~~~~~
    
    Here are only some tests witch doesn't work in the cross compare tests.
    
    Info: There exist some situations with different whitespace handling
        between creol2html and html2creole.

    Test the creole markup.
    

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate:$
    $Rev:$
    $Author: JensDiemer $

    :copyleft: 2008-2009 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE.txt for more details.
"""

import unittest
import StringIO

from tests.utils.base_unittest import BaseCreoleTest

from creole import creole2html




class TestCreole2htmlMacro(unittest.TestCase):
    """
    Tests around creole2html macro function.
    """
    def test_stderr(self):
        """
        Test if the traceback information send to a stderr handler.
        """
        my_stderr = StringIO.StringIO()
        creole2html(
            markup_string="<<notexist1>><<notexist2>><</notexist2>>",
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
            markup_string="<<html>><p>foo</p><</html>><p>bar</p>",
            verbose=1, 
#            stderr=sys.stderr, debug=False
        )
        self.assertEqual(html, u'<p>foo</p><p>&lt;p&gt;bar&lt;/p&gt;</p>\n')
    
    def test_default_macro2(self):
        html = creole2html(
            markup_string="<<html>>{{{&lt;nocode&gt;}}}<</html>>",
            verbose=1, 
#            stderr=sys.stderr, debug=False
        )
        self.assertEqual(html, u'{{{&lt;nocode&gt;}}}')
        
    def test_own_macro(self):
        """
        simple test for the "macro API"
        """
        class TestMacro(object):
            def test(self, args, text):
                return u"XXX%sXXX" % text
        
        html = creole2html(
            markup_string="<<test>>foo<</test>>",
            macros=TestMacro()
        )
        self.assertEqual(html, u'XXXfooXXX')





class TestCreole2html(BaseCreoleTest):

    def assertCreole(self, *args, **kwargs):
        self.assert_Creole2html(*args, **kwargs)

    #--------------------------------------------------------------------------

    def test_creole_basic(self):
        out_string = creole2html("a text line.")
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
            
            html code must start and end with a tag:
            <p>this <strong class="my">html code</strong> line pass-through</p>
            this works.

            this:
            <p>didn't<br />
            match</p>
            
            <p>
                didn't match
            </p>
            
            <p>didn't match,too.< p >
        """, """
            <p>This is a normal Text block witch would<br />
            escape html chars like &lt; and &gt; ;)</p>
            
            <p>html code must start and end with a tag:</p>
            <p>this <strong class="my">html code</strong> line pass-through</p>
            <p>this works.</p>
            
            <p>this:<br />
            &lt;p&gt;didn\'t&lt;br /&gt;<br />
            match&lt;/p&gt;</p>
            
            <p>&lt;p&gt;<br />
                didn\'t match<br />
            &lt;/p&gt;</p>
            
            <p>&lt;p&gt;didn\'t match,too.&lt; p &gt;</p>
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
            Bold and italics should //be
            able// to cross lines.

            But, should //not be...

            ...able// to cross paragraphs.
        """, """
            <p>Bold and italics should <i>be<br />
            able</i> to cross lines.</p>
            
            <p>But, should <i>not be...</i></p>
            
            <p>...able<i> to cross paragraphs.</i></p>
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
        
    def test_macro_html1(self):
        self.assertCreole(r"""
            html macro:
            <<html>>
            <p><<this is broken 'html', but it will be pass throu>></p>
            <</html>>
        """, r"""
            <p>html macro:</p>
            <p><<this is broken 'html', but it will be pass throu>></p>
        """, #debug=True
        )
        
    
    def test_macro_html2(self):
        """
        FIXME: Inline macro doesn't work :(
        """
        self.assertCreole(r"""
            Creole <<html>>&#x7B;...&#x7D;<</html>> code
        """, r"""
            <p>Creole</p>
            &#x7B;...&#x7D;
            <p>code</p>
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
        

    def test_django(self):
        self.assertCreole(r"""
            One {% inline tag 1 %} in text.
            
            {% a single tag %}
            
            Text before...
            {% block %}
            a block tag
            {% endblock %}
            ...and after
        """, r"""
            <p>One {% inline tag 1 %} in text.</p>
            
            {% a single tag %}
            
            <p>Text before...</p>
            {% block %}
            a block tag
            {% endblock %}
            
            <p>...and after</p>
        """, #debug=True
        )


if __name__ == '__main__':
    unittest.main()
#if __name__ == '__main__':
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreole2html)
#    unittest.TextTestRunner().run(suite)
