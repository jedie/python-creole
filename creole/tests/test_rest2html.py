#!/usr/bin/env python
# coding: utf-8

"""
    rest2html unittest
    ~~~~~~~~~~~~~~~~~~
    
    Unittests for rest2html, see: creole/rest2html/clean_writer.py

    :copyleft: 2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import unittest

from creole.tests.utils.base_unittest import BaseCreoleTest


class ReSt2HtmlTests(BaseCreoleTest):
    def test_clean_link_table(self):
        self.assert_rest2html("""
            :homepage:
              http://code.google.com/p/python-creole/
            
            :sourcecode:
              http://github.com/jedie/python-creole
        """, """
            <table>
            <tr><th>homepage:</th><td><a href="http://code.google.com/p/python-creole/">http://code.google.com/p/python-creole/</a></td>
            </tr>
            <tr><th>sourcecode:</th><td><a href="http://github.com/jedie/python-creole">http://github.com/jedie/python-creole</a></td>
            </tr>
            </table>
        """)

    def test_clean_table(self):
        self.assert_rest2html("""
            +------------+------------+
            | Headline 1 | Headline 2 |
            +============+============+
            | cell one   | cell two   |
            +------------+------------+
        """, """
            <table>
            <tr><th>Headline 1</th>
            <th>Headline 2</th>
            </tr>
            <tr><td>cell one</td>
            <td>cell two</td>
            </tr>
            </table>
        """)

    def test_clean_list(self):
        self.assert_rest2html("""
            * item 1
            
                * item 1.1
                
                * item 1.2
            
            * item 2
            
            numbered list:
            
            #. item A
        
            #. item B
        """, """
            <ul>
            <li><p>item 1</p>
            <ul>
            <li>item 1.1</li>
            <li>item 1.2</li>
            </ul>
            </li>
            <li><p>item 2</p>
            </li>
            </ul>
            <p>numbered list:</p>
            <ol>
            <li>item A</li>
            <li>item B</li>
            </ol>
        """)

    def test_clean_headline(self):
        self.assert_rest2html("""
            ======
            head 1
            ======
            
            ------
            head 2
            ------
        """, """
            <h1>head 1</h1>
            <h2>head 2</h2>
        """)


if __name__ == '__main__':
    unittest.main()
