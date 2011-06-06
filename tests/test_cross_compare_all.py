#!/usr/bin/env python
# coding: utf-8

"""
    cross compare unittest
    ~~~~~~~~~~~~~~~~~~~~~~
    
    Compare all similarities between:
        * creole2html
        * html2creole
        * textile2html (used the python textile module)
        * html2textile

    Note: This only works fine if there is no problematic whitespace handling.
        In this case, we must test in test_creole2html.py or test_html2creole.py

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import unittest



from tests.utils.base_unittest import BaseCreoleTest


class CrossCompareTests(BaseCreoleTest):
    """
    Cross compare tests for creol2html _and_ html2creole with the same test
    strings. Used BaseCreoleTest.assertCreole()
    """
    def test_bold_italics(self):
        self.cross_compare(
            creole_string=r"""
                **//bold italics//**
                //**bold italics**//
                //This is **also** good.//
            """,
            textile_string="""
                *__bold italics__*
                __*bold italics*__
                __This is *also* good.__
            """,
            html_string="""
                <p><strong><i>bold italics</i></strong><br />
                <i><strong>bold italics</strong></i><br />
                <i>This is <strong>also</strong> good.</i></p>
            """
        )

    def test_headlines1(self):
        self.cross_compare(
            creole_string=r"""
                = Level 1 (largest)
                
                == Level 2
                
                === Level 3
                
                ==== Level 4
                
                ===== Level 5
                
                ====== Level 6
            """,
            textile_string="""
                h1. Level 1 (largest)
                
                h2. Level 2
                
                h3. Level 3
                
                h4. Level 4
                
                h5. Level 5
                
                h6. Level 6
            """,
            html_string="""
                <h1>Level 1 (largest)</h1>
                
                <h2>Level 2</h2>
                
                <h3>Level 3</h3>
                
                <h4>Level 4</h4>
                
                <h5>Level 5</h5>
                
                <h6>Level 6</h6>
            """
        )

    def test_links(self):
        self.cross_compare(
            creole_string=r"""
                1 [[internal]] link.                
                2 [[http://domain.tld|link B]] test.
                3 [[http://de.wikipedia.org/wiki/Creole_(Markup)|Creole@wikipedia]]
                4 [[Foo://bar|unknown protocol]]
            """,
            textile_string="""
                1 "internal":internal link.
                2 "link B":http://domain.tld test.
                3 "Creole@wikipedia":http://de.wikipedia.org/wiki/Creole_(Markup)
                4 "unknown protocol":Foo://bar
            """,
            html_string="""
                <p>1 <a href="internal">internal</a> link.<br />
                2 <a href="http://domain.tld">link B</a> test.<br />
                3 <a href="http://de.wikipedia.org/wiki/Creole_(Markup)">Creole@wikipedia</a><br />
                4 <a href="Foo://bar">unknown protocol</a></p>
            """
        )

    def test_image(self):
        self.cross_compare(
            creole_string=r"""
                a {{/image.jpg|JPG pictures}} and
                a {{/image.jpeg|JPEG pictures}} and
                a {{/image.gif|GIF pictures}} and
                a {{/image.png|PNG pictures}} !
                {{/path1/path2/image|Image without files ext?}}
                [[http://example.com/|{{myimage.jpg|example site}}]]
            """,
            textile_string="""
                a !/image.jpg(JPG pictures)! and
                a !/image.jpeg(JPEG pictures)! and
                a !/image.gif(GIF pictures)! and
                a !/image.png(PNG pictures)! !
                !/path1/path2/image(Image without files ext?)!
                "!myimage.jpg(example site)!":http://example.com/
            """,
            html_string="""
                <p>a <img src="/image.jpg" title="JPG pictures" alt="JPG pictures" /> and<br />
                a <img src="/image.jpeg" title="JPEG pictures" alt="JPEG pictures" /> and<br />
                a <img src="/image.gif" title="GIF pictures" alt="GIF pictures" /> and<br />
                a <img src="/image.png" title="PNG pictures" alt="PNG pictures" /> !<br />
                <img src="/path1/path2/image" title="Image without files ext?" alt="Image without files ext?" /><br />
                <a href="http://example.com/"><img src="myimage.jpg" title="example site" alt="example site" /></a></p>
            """
        )

    def test_pre1(self):
        self.cross_compare(
            creole_string=r"""
                {{{
                * no list
                }}}
                """,
            textile_string="""
                <pre>
                * no list
                </pre>
                """,
            html_string="""
                <pre>
                * no list
                </pre>
            """)

    def test_pre2(self):
        """ TODO: html2creole: wrong lineendings """
        self.cross_compare(
            creole_string=r"""
                start
                
                {{{
                * no list
                }}}
                
                end
                """,
            textile_string="""
                start
                
                <pre>
                * no list
                </pre>
                
                end
                """,
            html_string="""
                <p>start</p>
                
                <pre>
                * no list
                </pre>
                
                <p>end</p>
            """)

    def test_pre_contains_braces(self):
        self.cross_compare(
            creole_string=r"""
                === Closing braces in nowiki:
                
                {{{
                if (x != NULL) {
                  for (i = 0) {
                    if (x = 1) {
                      x[i]--;
                  }}}
                }}}
                """,
            textile_string="""
                h3. Closing braces in nowiki:
                
                <pre>
                if (x != NULL) {
                  for (i = 0) {
                    if (x = 1) {
                      x[i]--;
                  }}}
                </pre>
                """,
            html_string="""
                <h3>Closing braces in nowiki:</h3>
                
                <pre>
                if (x != NULL) {
                  for (i = 0) {
                    if (x = 1) {
                      x[i]--;
                  }}}
                </pre>
            """)

    def test_list(self):
        """ Bold, Italics, Links, Pre in Lists """
        self.cross_compare(
            creole_string=r"""
                * **bold** item
                * //italic// item
    
                # item about a [[/foo/bar|certain_page]]
                """,
            textile_string="""
                * *bold* item
                * __italic__ item
    
                # item about a "certain_page":/foo/bar
            """,
            html_string="""
                <ul>
                  <li><strong>bold</strong> item</li>
                  <li><i>italic</i> item</li>
                </ul>
                <ol>
                  <li>item about a <a href="/foo/bar">certain_page</a></li>
                </ol>
            """,
            strip_lines=True
        )

    def test_simple_table(self):
        self.cross_compare(
            creole_string=r"""
                A simple table:
    
                |= Headline 1 |= Headline 2 |
                | cell one    | cell two    |
                """,
            textile_string="""
                A simple table:
                
                |_. Headline 1|_. Headline 2|
                |cell one|cell two|
                """,
            html_string="""
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
            """,
            strip_lines=True
            #debug=True
        )

if __name__ == '__main__':
    unittest.main()
