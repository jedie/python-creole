#!/usr/bin/env python
# coding: utf-8

"""
    html2creole tests
    ~~~~~~~~~~~~~~~~~
    
    special html to creole convert tests, witch can't tests in "cross compare"
    

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE.txt for more details.
"""

import sys
import unittest

from tests.utils.base_unittest import BaseCreoleTest

from creole import html2creole
from creole.html2creole import RAISE_UNKNOWN_NODES, HTML_MACRO_UNKNOWN_NODES, \
                                                            ESCAPE_UNKNOWN_NODES


class TestHtml2Creole(unittest.TestCase):
    """
    Tests around html2creole API.
    """
    pass




class TestHtml2CreoleMarkup(BaseCreoleTest):

    def assertCreole(self, raw_markup, raw_html, debug=False, **kwargs):
        self.assert_html2Creole(raw_markup, raw_html, debug=debug, **kwargs)

    #--------------------------------------------------------------------------

    def test_not_used(self):
        """
        Some other html tags -> convert.
        """
        self.assertCreole(r"""
            **Bold text**
            **Big text**
            //em tag//
            //italic//
        """, """
            <p><b>Bold text</b><br />
            <big>Big text</big><br />
            <em>em tag</em><br />
            <i>italic</i></p>
        """)

    def test_raise_unknown_node(self):
        """
        Test creole.html2creole.RAISE_UNKNOWN_NODES mode:
        Raise NotImplementedError on unknown tags.
        """
        self.assertRaises(NotImplementedError,
            html2creole,
            html_string=u"<unknwon>",
            unknown_emit=RAISE_UNKNOWN_NODES
        )

    def test_escape_unknown_nodes(self):
        """
        Test creole.html2creole.ESCAPE_UNKNOWN_NODES mode:
        All unknown tags should be escaped.
        """
        self.assertCreole(r"""
            111 &lt;unknown&gt;foo&lt;/unknown&gt; 222
            333&lt;unknown foo1="bar1" foo2="bar2"&gt;foobar&lt;/unknown&gt;444

            555&lt;unknown /&gt;666
        """, """
            <p>111 <unknown>foo</unknown> 222<br />
            333<unknown foo1="bar1" foo2="bar2">foobar</unknown>444</p>

            <p>555<unknown />666</p>
        """,
            unknown_emit=ESCAPE_UNKNOWN_NODES
        )

    def test_entities(self):
        """
        Test html entities.

        copyright sign is in Latin-1 Supplement:
            http://pylucid.org/_command/144/DecodeUnicode/display/1/
        Box Drawing:
            http://pylucid.org/_command/144/DecodeUnicode/display/66/
        """
        self.assertCreole(u"""
            * less-than sign: < < <
            * greater-than sign: > > >
            * copyright sign: © ©
            * box drawing: ╬ ╬
            * german umlauts: ä ö ü
        """, """
            <ul>
            <li>less-than sign: &lt; &#60; &#x3C;</li>
            <li>greater-than sign: &gt; &#62; &#x3E;</li>
            <li>copyright sign: &#169; &#xA9;</li>
            <li>box drawing: &#9580; &#x256C;</li>
            <li>german umlauts: &auml; &ouml; &uuml;</li>
            </ul>
        """)

    def test_html_entity_nbsp(self):
        """ Non breaking spaces is not in htmlentitydefs """
        self.assertCreole(r"""
            a non braking space: [ ] !
        """, """
            <p>a non braking space: [&nbsp;] !</p>
        """)

    def test_html_entity_in_pre(self):
        self.assertCreole(r"""
            {{{<code>{% lucidTag RSS url="http url" %}</code>}}}
        """, """
            <pre><code>&#x7B;% lucidTag RSS url="http url" %&#x7D;</code></pre>
        """)

    def test_unknown_entity(self):
        """
        Test a unknown html entity.
        FIXME: What sould happend?
        """
        self.assertCreole(r"""
            copy&paste
        """, """
            <p>copy&paste</p>
        """)
        self.assertCreole(r"""
            [[/url/|Search & Destroy]]
        """, """
            <a href="/url/">Search & Destroy</a>
        """)

    def test_tbody_table(self):
        self.assertCreole(r"""
            Ignore 'tbody' tag in tables:
            
            |= Headline 1 |= Headline 2 |
            | cell one    | cell two    |
            end
        """, """
            <p>Ignore 'tbody' tag in tables:</p>
            <table>
            <tbody>
            <tr>
                <th>Headline 1</th>
                <th>Headline 2</th>
            </tr>
            <tr>
                <td>cell one</td>
                <td>cell two</td>
            </tr>
            </tbody>
            </table>
            <p>end</p>
        """)

    def test_p_table(self):
        """ strip <p> tags in table cells """
        self.assertCreole(r"""
            | cell one | cell two\\new line |
        """, """
            <table>
            <tr>
                <td><p>cell one</p></td>
                <td><p>cell two</p><p>new line</p><p></p></td>
            </tr>
            </table>
        """)

    def test_image(self):
        """ test image tag with different alt/title attribute """
        self.assertCreole(r"""
            {{foobar1.jpg|foobar1.jpg}}
            {{/foobar2.jpg|foobar2.jpg}}
            {{/path1/path2/foobar3.jpg|foobar3.jpg}}
            {{/foobar4.jpg|It's foobar 4}}
            {{/foobar5.jpg|It's foobar 5}}
            {{/foobar6.jpg|a long picture title}}
        """, """
            <p><img src="foobar1.jpg" /><br />
            <img src="/foobar2.jpg" /><br />
            <img src="/path1/path2/foobar3.jpg" /><br />
            <img src="/foobar4.jpg" alt="It's foobar 4" /><br />
            <img src="/foobar5.jpg" title="It's foobar 5" /><br />
            <img src="/foobar6.jpg" alt="short name" title="a long picture title" /></p>
        """)

    def test_non_closed_br(self):
        self.assertCreole(r"""
            one
            two
        """, """
            <p>one<br>
            two</p>
        """)

    def test_explicit_closed_br(self):
        self.assertCreole(r"""
            one
            two
        """, """
            <p>one<br></br>
            two</p>
        """)

    def test_newline_before_list(self):
        """
        http://code.google.com/p/python-creole/issues/detail?id=16
        """
        self.assertCreole(r"""
            **foo**
            
            * one
        """, """
            <b>foo</b><ul><li>one</li></ul>
        """)

    #--------------------------------------------------------------------------
    # TODOs:


    def test_newline_before_headline(self):
        """ TODO: http://code.google.com/p/python-creole/issues/detail?id=16#c5 """
        self.assertCreole(r"""
            **foo**
            
            = one
        """, """
            <b>foo</b>
            <h1>one</h1>
        """)#, debug=True)

    def test_cross_lines(self):
        """ TODO: bold/italics cross lines
        see: http://code.google.com/p/python-creole/issues/detail?id=13 
        """
        self.assertCreole(r"""
            Bold and italics should //be
            able// to **cross
            lines.**
        """, """
            <p>Bold and italics should <i>be<br />
            able</i> to <strong>cross<br />
            lines.</strong></p>
        """)


    def test_no_space_before_blocktag(self):
        """ TODO: Bug in html2creole.strip_html(): Don't add a space before/after block tags """
        self.assertCreole(r"""
            **foo**
            
            * one
        """, """
            <b>foo</b>
            <ul><li>one</li></ul>
        """)#, debug=True)


    def test_format_in_a_text(self):
        """ TODO: http://code.google.com/p/python-creole/issues/detail?id=4 """
        self.assertCreole(r"""
            **[[/url/|title]]**
        """, """
            <a href="/url/"><strong>title</strong></a>
        """)


#    def test_links(self):
#        self.assertCreole(r"""
#            test link: '[[internal links|link A]]' 1 and
#            test link: '[[http://domain.tld|link B]]' 2.
#        """, """
#            <p>test link: '<a href="internal links">link A</a>' 1 and<br />
#            test link: '<a href="http://domain.tld">link B</a>' 2.</p>
#        """)
#
#    def test_images(self):
#        self.assertCreole(r"""
#            a {{/image.jpg|JPG pictures}} and
#            a {{/image.jpeg|JPEG pictures}} and
#            a {{/image.gif|GIF pictures}} and
#            a {{/image.png|PNG pictures}} !
#
#            picture [[www.domain.tld|{{foo.JPG|Foo}}]] as a link
#        """, """
#            <p>a <img src="/image.jpg" alt="JPG pictures"> and<br />
#            a <img src="/image.jpeg" alt="JPEG pictures"> and<br />
#            a <img src="/image.gif" alt="GIF pictures" /> and<br />
#            a <img src="/image.png" alt="PNG pictures" /> !</p>
#
#            <p>picture <a href="www.domain.tld"><img src="foo.JPG" alt="Foo"></a> as a link</p>
#        """)
#
#    def test_nowiki1(self):
#        self.assertCreole(r"""
#            this:
#            {{{
#            //This// does **not** get [[formatted]]
#            }}}
#            and this: {{{** <i>this</i> ** }}} not, too.
#
#            === Closing braces in nowiki:
#            {{{
#            if (x != NULL) {
#              for (i = 0; i < size; i++) {
#                if (x[i] > 0) {
#                  x[i]--;
#              }}}
#            }}}
#        """, """
#            <p>this:</p>
#            <pre>
#            //This// does **not** get [[formatted]]
#            </pre>
#            <p>and this: <tt>** &lt;i&gt;this&lt;/i&gt; ** </tt> not, too.</p>
#
#            <h3>Closing braces in nowiki:</h3>
#            <pre>
#            if (x != NULL) {
#              for (i = 0; i &lt; size; i++) {
#                if (x[i] &gt; 0) {
#                  x[i]--;
#              }}}
#            </pre>
#        """)
#

#
#    def test_horizontal_rule(self):
#        self.assertCreole(r"""
#            one
#            ----
#            two
#        """, """
#            <p>one</p>
#            <hr />
#            <p>two</p>
#        """)
#
#    def test_list1(self):
#        """
#        FIXME: Two newlines between a list and the next paragraph :(
#        """
#        self.assertCreole(r"""
#            ==== List a:
#            * a1 item
#            ** a1.1 Force\\linebreak
#            ** a1.2 item
#            *** a1.2.1 item
#            *** a1.2.2 item
#            * a2 item
#
#
#            list 'a' end
#
#            ==== List b:
#            # b1 item
#            ## b1.2 item
#            ### b1.2.1 item
#            ### b1.2.2 Force\\linebreak1\\linebreak2
#            ## b1.3 item
#            # b2 item
#
#
#            list 'b' end
#        """, """
#            <h4>List a:</h4>
#            <ul>
#            <li>a1 item</li>
#            <ul>
#                <li>a1.1 Force
#                linebreak</li>
#                <li>a1.2 item</li>
#                <ul>
#                    <li>a1.2.1 item</li>
#                    <li>a1.2.2 item</li>
#                </ul>
#            </ul>
#            <li>a2 item</li>
#            </ul>
#            <p>list 'a' end</p>
#
#            <h4>List b:</h4>
#            <ol>
#            <li>b1 item</li>
#            <ol>
#                <li>b1.2 item</li>
#                <ol>
#                    <li>b1.2.1 item</li>
#                    <li>b1.2.2 Force
#                    linebreak1
#                    linebreak2</li>
#                </ol>
#                <li>b1.3 item</li>
#            </ol>
#            <li>b2 item</li>
#            </ol>
#            <p>list 'b' end</p>
#        """,
##            debug=True
#        )
#
#    def test_list2(self):
#        """ Bold, Italics, Links, Pre in Lists """
#        self.assertCreole(r"""
#            * **bold** item
#            * //italic// item
#
#            # item about a [[domain.tld|page link]]
#            # {{{ //this// is **not** [[processed]] }}}
#        """, """
#            <ul>
#                <li><strong>bold</strong> item</li>
#                <li><i>italic</i> item</li>
#            </ul>
#            <ol>
#                <li>item about a <a href="domain.tld">page link</a></li>
#                <li><tt>//this// is **not** [[processed]]</tt></li>
#            </ol>
#        """,
##            debug=True
#        )
#
#    #__________________________________________________________________________
#    # TODO:
#
#    def test_escape_char(self):
#        self.assertCreole(r"""
#            ~#1
#            http://domain.tld/~bar/
#            ~http://domain.tld/
#            [[Link]]
#            ~[[Link]]
#        """, """
#            <p>#1<br />
#            <a href="http://domain.tld/~bar/">http://domain.tld/~bar/</a><br />
#            http://domain.tld/<br />
#            <a href="Link">Link</a><br />
#            [[Link]]</p>
#        """)

if __name__ == '__main__':
    unittest.main()
#if __name__ == '__main__':
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestHtml2Creole)
#    unittest.TextTestRunner().run(suite)
