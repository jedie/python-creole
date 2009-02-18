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

import sys
import unittest

from tests.utils.base_unittest import BaseCreoleTest

from creole import creole2html



class TestCreole2html(BaseCreoleTest):

    def assertCreole(self, source_string, should_string, debug=False):
        self.assert_Creole2html(source_string, should_string, debug)

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
        
    def test_macro_html(self):
        self.assertCreole(r"""
            html macro:
            <<html>>
            <p><<this is broken 'html'>></p>
            <</html>>
        """, r"""
            <p>html macro:</p>
            <p><<this is broken 'html'>></p>
        """, #debug=True
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
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreole2html)
    unittest.TextTestRunner().run(suite)
