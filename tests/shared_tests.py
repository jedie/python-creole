#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    PyLucid unittest
    ~~~~~~~~~~~~~~~~



    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate: 2008-11-14 12:05:22 +0100 (Fr, 14 Nov 2008) $
    $Rev: 1795 $
    $Author: JensDiemer $

    :copyleft: 2008 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3, see LICENSE.txt for more details.
"""

import sys
import unittest

from utils import MarkupTest

from creole import creole2html, html2creole


class SharedTests(MarkupTest):
    def _debug_text(self, msg, raw_text):
        text = raw_text.replace(" ", ".")
        text = text.replace("\n", "\\n\n")
        text = text.replace("\t", "\\t")
        
        print "_"*79
        print " Debug Text: %s" % msg
        print text
        print "-"*79
        
    def assert_Creole2html(self, source_string, should_string, debug=False):
        # prepare whitespace on test strings
        markup_string = self._prepare_text(source_string)
        
        should = self._prepare_text(should_string)
        if debug:
            self._debug_text("assert_Creole2html() should_string", should)
        
        # convert creole markup into html code
        out_string = creole2html(markup_string)
        if debug:
            self._debug_text("assert_Creole2html() creole2html", out_string)
        
        out_string = out_string.rstrip("\n")
        out_string = out_string.replace("\t", "    ")
        
        # compare
        self.assertEqual(out_string, should)
        
    def assert_html2Creole(self, raw_markup, raw_html, debug=False):
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


    def test_bold_italics(self):
        self.assertCreole(r"""
            **//bold italics//**
            //**bold italics**//
            //This is **also** good.//
        """, """
            <p><strong><i>bold italics</i></strong><br />
            <i><strong>bold italics</strong></i><br />
            <i>This is <strong>also</strong> good.</i></p>
        """)

    def test_internal_links(self):
        self.assertCreole(r"""
            A [[internal]] link...
            ...and [[/a internal]] link.
        """, """
            <p>A <a href="internal">internal</a> link...<br />
            ...and <a href="/a internal">/a internal</a> link.</p>
        """)
        
    def test_external_links(self):
        self.assertCreole(r"""
            With pipe separator:
            1 [[internal links|link A]] test.
            2 [[http://domain.tld|link B]] test.
        """, """
            <p>With pipe separator:<br />
            1 <a href="internal links">link A</a> test.<br />
            2 <a href="http://domain.tld">link B</a> test.</p>
        """)

    def test_bolditalic_links(self):
        self.assertCreole(r"""
            //[[a internal]]//
            **[[Shortcut2|a page2]]**
            //**[[Shortcut3|a page3]]**//
        """, """
            <p><i><a href="a internal">a internal</a></i><br />
            <strong><a href="Shortcut2">a page2</a></strong><br />
            <i><strong><a href="Shortcut3">a page3</a></strong></i></p>
        """)
        
    def test_image(self):
        self.assertCreole(r"""
            a {{/image.jpg|JPG pictures}} and
            a {{/image.jpeg|JPEG pictures}} and
            a {{/image.gif|GIF pictures}} and
            a {{/image.png|PNG pictures}} !
        """, """
            <p>a <img src="/image.jpg" alt="JPG pictures"> and<br />
            a <img src="/image.jpeg" alt="JPEG pictures"> and<br />
            a <img src="/image.gif" alt="GIF pictures"> and<br />
            a <img src="/image.png" alt="PNG pictures"> !</p>
        """)
            
    def test_django1(self):
        """
        Test if django template tags are not changed by Creole.
        The Creole image tag use "{{" and "}}", too.
        We test also the passthrough for all django template blocktags
        """
        self.assertCreole(r"""
            The current page name: >{{ PAGE.name }}< great?
            A {% lucidTag page_update_list count=10 %} PyLucid plugin
            
            {% block %}
            FooBar
            {% endblock %}
            
            A [[www.domain.tld|link]].
            a {{/image.jpg|My Image}} image

            no image: {{ foo|bar }}!
            picture [[www.domain.tld|{{foo.JPG|Foo}}]] as a link
        """, """
            <p>The current page name: &gt;{{ PAGE.name }}&lt; great?<br />
            A {% lucidTag page_update_list count=10 %} PyLucid plugin</p>
            
            {% block %}
            FooBar
            {% endblock %}
            
            <p>A <a href="www.domain.tld">link</a>.<br />
            a <img src="/image.jpg" alt="My Image"> image</p>
            
            <p>no image: {{ foo|bar }}!<br />
            picture <a href="www.domain.tld"><img src="foo.JPG" alt="Foo"></a> as a link</p>
        """)

    def test_django2(self):
        self.assertCreole(r"""
            ==== Headline 1

            On {% a tag 1 %} line
            line two
            
            ==== Headline 2
            
            {% a tag 2 %}
            
            Right block with a end tag:
            
            {% block %}
            <Foo:> {{ Bar }}
            {% endblock %}
            
            A block without the right end block:
            
            {% block1 %}
            not matched
            {% endblock2 %}
            
            A block without endblock:
            {% noblock3 %}
            not matched
            {% noblock3 %}
            CCC
        """, """
            <h4>Headline 1</h4>
            
            <p>On {% a tag 1 %} line<br />
            line two</p>
            
            <h4>Headline 2</h4>
            
            {% a tag 2 %}
            
            <p>Right block with a end tag:</p>
            
            {% block %}
            <Foo:> {{ Bar }}
            {% endblock %}
            
            <p>A block without the right end block:</p>
            
            <p>{% block1 %}<br />
            not matched<br />
            {% endblock2 %}</p>
            
            <p>A block without endblock:<br />
            {% noblock3 %}<br />
            not matched<br />
            {% noblock3 %}<br />
            CCC</p>
        """,
        #debug=True
        )

    def test_nowiki1(self):
        self.assertCreole(r"""
            this:
            
            {{{
            //This// does **not** get [[formatted]]
            }}}
            and this: {{{ ** <i>this</i> ** }}}
            
            === Closing braces in nowiki:
            
            {{{
            if (x != NULL) {
              for (i = 0; i < size; i++) {
                if (x[i] > 0) {
                  x[i]--;
              }}}
            }}}
        """, """
            <p>this:</p>
            
            <pre>
            //This// does **not** get [[formatted]]
            </pre>
            <p>and this: <tt>** &lt;i&gt;this&lt;/i&gt; **</tt></p>
            
            <h3>Closing braces in nowiki:</h3>
            
            <pre>
            if (x != NULL) {
              for (i = 0; i &lt; size; i++) {
                if (x[i] &gt; 0) {
                  x[i]--;
              }}}
            </pre>
        """)

    def test_nowiki2(self):
        self.assertCreole(r"""
            111
            222
            
            {{{
            333
            }}}
            444

            one
            
            {{{
            foobar
            }}}
            two
        """, """
            <p>111<br />
            222</p>
            
            <pre>
            333
            </pre>
            <p>444</p>
            
            <p>one</p>
            
            <pre>
            foobar
            </pre>
            <p>two</p>
        """)


    def test_headlines(self):
        self.assertCreole(r"""
            = Level 1 (largest)
            
            == Level 2
            
            === Level 3
            
            ==== Level 4
            
            ===== Level 5
            
            ====== Level 6
            
            === **not** \\ //parsed//
            
            No == headline == or?
        """, r"""
            <h1>Level 1 (largest)</h1>
            
            <h2>Level 2</h2>
            
            <h3>Level 3</h3>
            
            <h4>Level 4</h4>
            
            <h5>Level 5</h5>
            
            <h6>Level 6</h6>
            
            <h3>**not** \\ //parsed//</h3>
            
            <p>No == headline == or?</p>
        """)

    def test_horizontal_rule(self):
        self.assertCreole(r"""
            one
            
            ----
            
            two
        """, """
            <p>one</p>
            
            <hr />

            <p>two</p>
        """)

    def test_bullet_list(self):
        self.assertCreole(r"""
            * Item 1
            ** Item 1.1
            ** a **bold** Item 1.2
            * Item 2
            ** Item 2.1
            *** [[a link Item 3.1]]
            *** Force\\linebreak 3.2
                *** item 3.3
              *** item 3.4
              
            up to five levels
            * 1
            ** 2
            *** 3
            **** 4
            ***** 5
        """, """
            <ul>
                <li>Item 1
                <ul>
                    <li>Item 1.1</li>
                    <li>a <strong>bold</strong> Item 1.2</li>
                </ul></li>
                <li>Item 2
                <ul>
                    <li>Item 2.1
                    <ul>
                        <li><a href="a link Item 3.1">a link Item 3.1</a></li>
                        <li>Force<br />
                        linebreak 3.2</li>
                        <li>item 3.3</li>
                        <li>item 3.4</li>
                    </ul></li>
                </ul></li>
            </ul>
            <p>up to five levels</p>
            <ul>
                <li>1
                <ul>
                    <li>2
                    <ul>
                        <li>3
                        <ul>
                            <li>4
                            <ul>
                                <li>5</li>
                            </ul></li>
                        </ul></li>
                    </ul></li>
                </ul></li>
            </ul>
        """)

    def test_number_list(self):
        self.assertCreole(r"""
            # Item 1
            ## Item 1.1
            ## a **bold** Item 1.2
            # Item 2
            ## Item 2.1
            ### [[a link Item 3.1]]
            ### Force\\linebreak 3.2
            ### item 3.3
            ### item 3.4
            
            up to five levels
            
            # 1
            ## 2
            ### 3
            #### 4
            ##### 5
        """, """
            <ol>
                <li>Item 1
                <ol>
                    <li>Item 1.1</li>
                    <li>a <strong>bold</strong> Item 1.2</li>
                </ol></li>
                <li>Item 2
                <ol>
                    <li>Item 2.1
                    <ol>
                        <li><a href="a link Item 3.1">a link Item 3.1</a></li>
                        <li>Force<br />
                        linebreak 3.2</li>
                        <li>item 3.3</li>
                        <li>item 3.4</li>
                    </ol></li>
                </ol></li>
            </ol>
            <p>up to five levels</p>
            
            <ol>
                <li>1
                <ol>
                    <li>2
                    <ol>
                        <li>3
                        <ol>
                            <li>4
                            <ol>
                                <li>5</li>
                            </ol></li>
                        </ol></li>
                    </ol></li>
                </ol></li>
            </ol>
        """,
        debug = True
        )
        
    def test_list(self):
        """ Bold, Italics, Links, Pre in Lists """
        self.assertCreole(r"""
            * **bold** item
            * //italic// item
            
            # item about a [[certain_page]]
            # {{{ //this// is **not** [[processed]] }}}
        """, """
            <ul>
                <li><strong>bold</strong> item</li>
                <li><i>italic</i> item</li>
            </ul>
            <ol>
                <li>item about a <a href="certain_page">certain_page</a></li>
                <li><tt>//this// is **not** [[processed]]</tt></li>
            </ol>
        """)

    def test_table1(self):
        self.assertCreole(r"""
            A simple table:
            
            |= Headline 1 |= Headline 2 |
            | cell one    | cell two    |
            ...end
        """, """
            <p>A simple table:</p>
            
            <table>
            <tr>
                <th>Headline 1</th>
                <th>Headline 2</th>
            </tr>
            <tr>
                <td>cell one</td>
                <td>cell two</td>
            </tr>
            </table>
            <p>...end</p>
        """)

    def test_table2(self):
        self.assertCreole(r"""
            A Table...
            
            |= Headline  |= a other\\headline    |= the **big end**     |
            | a cell     | a **big** cell        | **//bold italics//** |
            | next\\line | No == headline == or? |                      |
            |            |                       | empty cells          |
            ...end
        """, """
            <p>A Table...</p>
            
            <table>
            <tr>
                <th>Headline</th>
                <th>a other<br />
                    headline</th>
                <th>the <strong>big end</strong></th>
            </tr>
            <tr>
                <td>a cell</td>
                <td>a <strong>big</strong> cell</td>
                <td><strong><i>bold italics</i></strong></td>
            </tr>
            <tr>
                <td>next<br />
                    line</td>
                <td>No == headline == or?</td>
                <td></td>
            </tr>
            <tr>
                <td></td>
                <td></td>
                <td>empty cells</td>
            </tr>
            </table>
            <p>...end</p>
        """,
            #debug=True
        )



        
#    def test_macro_html1(self):
#        self.assertCreole(r"""
#            <<a_not_existing_macro>>
#            
#            <<code>>
#            some code
#            <</code>>
#            
#            a macro:
#            <<code>>
#            <<code>>
#            the sourcecode
#            <</code>>
#        """, r"""
#            <p>[Error: Macro 'a_not_existing_macro' doesn't exist]</p>
#            <fieldset class="pygments_code">
#            <legend class="pygments_code"><small title="no lexer matching the text found">unknown type</small></legend>
#            <pre><code>some code</code></pre>
#            </fieldset>
#            <p>a macro:</p>
#            <fieldset class="pygments_code">
#            <legend class="pygments_code"><small title="no lexer matching the text found">unknown type</small></legend>
#            <pre><code>&lt;&lt;code&gt;&gt;
#            the sourcecode</code></pre>
#            </fieldset>
#        """)
        
    def test_macro_html2(self):
        self.assertCreole(r"""
            html macro:
            <<html>>
            <p><<this is 'html'>></p>
            <</html>>
        """, r"""
            <p>html macro:</p>
            <p><<this is 'html'>></p>
        """)

#    def test_macro_pygments_code(self):
#        self.assertCreole(r"""
#            a macro:
#            <<code ext=.css>>
#            /* Stylesheet */
#            form * {
#              vertical-align:middle;
#            }
#            <</code>>
#            the end
#        """, """
#            <p>a macro:</p>
#            <fieldset class="pygments_code">
#            <legend class="pygments_code">CSS</legend><table class="pygmentstable"><tr><td class="linenos"><pre>1
#            2
#            3
#            4</pre></td><td class="code"><div class="pygments"><pre><span class="c">/* Stylesheet */</span>
#            <span class="nt">form</span> <span class="o">*</span> <span class="p">{</span>
#              <span class="k">vertical-align</span><span class="o">:</span><span class="k">middle</span><span class="p">;</span>
#            <span class="p">}</span>
#            </pre></div>
#            </td></tr></table></fieldset>
#            <p>the end</p>
#        """)




if __name__ == '__main__':
    unittest.main()