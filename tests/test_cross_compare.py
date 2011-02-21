#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    cross compare unittest
    ~~~~~~~~~~~~~~~~~~~~~~

    Here we test both ways creol2html _and_ html2creole with the same given
    refenrece strings.

    Note: This only works fine if there is no problematic whitespace handling.
        In this case, we must test in test_creole2html.py or test_html2creole.py

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate$
    $Rev$
    $Author$

    :copyleft: 2008-2009 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE.txt for more details.
"""

import unittest

from tests.utils.base_unittest import BaseCreoleTest

from creole.html2creole import RAISE_UNKNOWN_NODES, HTML_MACRO_UNKNOWN_NODES, \
                                                        ESCAPE_UNKNOWN_NODES


class CrossCompareTests(BaseCreoleTest):
    """
    Cross compare tests for creol2html _and_ html2creole with the same test
    strings. Used BaseCreoleTest.assertCreole()
    """
    def test_typeface(self):
        self.assertCreole(r"""
            basics:
            **//bold italics//**
            //**bold italics**//
            //This is **also** good.//

            Creole 1.0 optional:
            This is ##monospace## text.
            This is ^^superscripted^^ text.
            This is ,,subscripted,, text.
            This is __underlined__ text.

            own additions:
            This is --small-- and this ~~strikeout~~ ;)
        """, """
            <p>basics:<br />
            <strong><i>bold italics</i></strong><br />
            <i><strong>bold italics</strong></i><br />
            <i>This is <strong>also</strong> good.</i></p>

            <p>Creole 1.0 optional:<br />
            This is <tt>monospace</tt> text.<br />
            This is <sup>superscripted</sup> text.<br />
            This is <sub>subscripted</sub> text.<br />
            This is <u>underlined</u> text.</p>

            <p>own additions:<br />
            This is <small>small</small> and this <del>strikeout</del> ;)</p>
        """)

    def test_small(self):
        """
        http://code.google.com/p/python-creole/issues/detail?id=12#c0
        """
        self.assertCreole(r"""
            no -- small
            no // italics
            no ** bold
            no ## monospace
            no ^^ superscripted
            no ,, subscripted
            no __ underline
        """, """
            <p>no -- small<br />
            no // italics<br />
            no ** bold<br />
            no ## monospace<br />
            no ^^ superscripted<br />
            no ,, subscripted<br />
            no __ underline</p>
        """, debug=False)

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
            3 [[http://de.wikipedia.org/wiki/Creole_(Markup)|Creole@wikipedia]]
        """, """
            <p>With pipe separator:<br />
            1 <a href="internal links">link A</a> test.<br />
            2 <a href="http://domain.tld">link B</a> test.<br />
            3 <a href="http://de.wikipedia.org/wiki/Creole_(Markup)">Creole@wikipedia</a></p>
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
            {{/path1/path2/image|Image without files ext?}}
            [[http://example.com/|{{myimage.jpg|example site}}]]
        """, """
            <p>a <img src="/image.jpg" alt="JPG pictures" /> and<br />
            a <img src="/image.jpeg" alt="JPEG pictures" /> and<br />
            a <img src="/image.gif" alt="GIF pictures" /> and<br />
            a <img src="/image.png" alt="PNG pictures" /> !<br />
            <img src="/path1/path2/image" alt="Image without files ext?" /><br />
            <a href="http://example.com/"><img src="myimage.jpg" alt="example site" /></a></p>
        """)

    def test_pre_contains_braces(self):
        self.assertCreole(r"""
            === Closing braces in nowiki:
            {{{
            if (x != NULL) {
              for (i = 0; i < size; i++) {
                if (x[i] > 0) {
                  x[i]--;
              }}}
            }}}
        """, """
            <h3>Closing braces in nowiki:</h3>
            <pre>
            if (x != NULL) {
              for (i = 0; i &lt; size; i++) {
                if (x[i] &gt; 0) {
                  x[i]--;
              }}}
            </pre>
        """)

    def test_pre2(self):
        self.assertCreole(r"""
            111
            
            {{{
            //This// does **not** get [[formatted]]
            }}}
            222

            one
            
            {{{
            foo

            bar
            }}}
            two
        """, """
            <p>111</p>
            
            <pre>
            //This// does **not** get [[formatted]]
            </pre>
            <p>222</p>
            
            <p>one</p>
            
            <pre>
            foo

            bar
            </pre>
            <p>two</p>
        """)

    def test_pre(self):
        self.assertCreole(r"""
            start
            
            {{{
            * no list
            <html escaped>
            }}}
            end
        """, """
            <p>start</p>
            
            <pre>
            * no list
            &lt;html escaped&gt;
            </pre>
            <p>end</p>
        """)

    def test_tt(self):
        self.assertCreole(r"""
            this is ##**strong** Teletyper## ;)
        """, """
            <p>this is <tt><strong>strong</strong> Teletyper</tt> ;)</p>
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
#        debug = True
        )

    def test_list(self):
        """ Bold, Italics, Links, Pre in Lists """
        self.assertCreole(r"""
            * **bold** item
            * //italic// item

            # item about a [[certain_page]]
        """, """
            <ul>
                <li><strong>bold</strong> item</li>
                <li><i>italic</i> item</li>
            </ul>
            <ol>
                <li>item about a <a href="certain_page">certain_page</a></li>
            </ol>
        """)

    def test_simple_table(self):
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

    def test_big_table(self):
        self.assertCreole(r"""
            A Table...

            |= Headline  |= a other\\headline    |= the **big end**     |
            | a cell     | a **big** cell        | **//bold italics//** |
            | next\\line | No == headline == or? |                      |
            | link test: | a [[/url/|link]] in   | a cell.              |
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
                <td>link test:</td>
                <td>a <a href="/url/">link</a> in</td>
                <td>a cell.</td>
            </tr>
            <tr>
                <td></td>
                <td></td>
                <td>empty cells</td>
            </tr>
            </table>
            <p>...end</p>
        """,
#            debug = True
        )

    def test_html_macro_unknown_nodes(self):
        """
        use the <<html>> macro to mask unknown tags.
        Note:
            All cross compare teste use html2creole.HTML_MACRO_UNKNOWN_NODES
        """
        self.assertCreole(r"""
            111 <<html>><x><</html>>foo<<html>></x><</html>> 222
            333<<html>><x foo1="bar1"><</html>>foobar<<html>></x><</html>>444

            555<<html>><x /><</html>>666
        """, """
            <p>111 <x>foo</x> 222<br />
            333<x foo1="bar1">foobar</x>444</p>

            <p>555<x />666</p>
        """)

    def test_entities(self):
        self.assertCreole(u"""
            less-than sign: <
            greater-than sign: >
        """, """
            <p>less-than sign: &lt;<br />
            greater-than sign: &gt;</p>
        """)

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
