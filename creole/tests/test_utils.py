#!/usr/bin/env python
# coding: utf-8

"""
    unittest for some utils
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import unittest

from creole.tests.utils.utils import MarkupTest
from creole.shared.markup_table import MarkupTable


class UtilsTests(MarkupTest):
    def assertEqual2(self, first, second, msg=""):
        self.assertNotEqual(first, second, msg)

#        first = self._prepare_text(first)
        second = self._prepare_text(second)

        self.assertEqual(first, second, msg)

    def test_markup_table_creole(self):
        t = MarkupTable(head_prefix="* ")
        t.add_tr()
        t.add_th("head1")
        t.add_th("head2")
        t.add_tr()
        t.add_td("1.1.")
        t.add_td("1.2.")
        t.add_tr()
        t.add_td("2.1.")
        t.add_td("2.2.")
        table = t.get_table_markup()

        self.assertEqual2(
            table,
            """
            |* head1 |* head2 |
            | 1.1.   | 1.2.   |
            | 2.1.   | 2.2.   |
            """
        )

    def test_markup_table_textile(self):
        t = MarkupTable(head_prefix="_. ", auto_width=False)
        t.add_tr()
        t.add_th("head1")
        t.add_th("head2")
        t.add_tr()
        t.add_td("1.1.")
        t.add_td("1.2.")
        t.add_tr()
        t.add_td("2.1.")
        t.add_td("2.2.")
        table = t.get_table_markup()

        self.assertEqual2(
            table,
            """
            |_. head1|_. head2|
            |1.1.|1.2.|
            |2.1.|2.2.|
            """
        )

    def test_markup_table_rest(self):
        t = MarkupTable(head_prefix="")
        t.add_tr()
        t.add_th("head1")
        t.add_th("head2")
        t.add_tr()
        t.add_td("1.1.")
        t.add_td("1.2.")
        t.add_tr()
        t.add_td("2.1.")
        t.add_td("2.2.")
        table = t.get_rest_table()

        self.assertEqual2(
            table,
            """
            +-------+-------+
            | head1 | head2 |
            +=======+=======+
            | 1.1.  | 1.2.  |
            +-------+-------+
            | 2.1.  | 2.2.  |
            +-------+-------+
            """
        )


if __name__ == '__main__':
    unittest.main()
