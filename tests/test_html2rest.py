#!/usr/bin/env python
# coding: utf-8

"""
    html2rest unittest
    ~~~~~~~~~~~~~~~~~~~~~
    
    Unittests for special cases which only works in the html2rest way.

    Note: This only works fine if there is no problematic whitespace handling.

    :copyleft: 2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import unittest

from creole.shared.unknown_tags import preformat_unknown_nodes
from tests.utils.base_unittest import BaseCreoleTest


class ReStTests(BaseCreoleTest):
    def test_line_breaks(self):
        """
        Line breaks in HTML are lost.
        """
        self.assert_html2rest(
            rest_string="""
                first block, line 1 and line 2
                
                second block, line 1 and line 2
            """,
            html_string="""
                <p>first block, line 1
                and line 2</p>
                <p>second block, line 1
                and line 2</p>
            """,
#            debug=True
        )

    def test_substitution_image_without_alt_or_title(self):
        self.assert_html2rest(
            rest_string="""
                A inline |image.png| image.

                .. |image.png| image:: /url/to/image.png

                ...and some text below.
            """,
            html_string="""
                <p>A inline <img src="/url/to/image.png" /> image.</p>
                <p>...and some text below.</p>
            """
        )

    def test_substitution_image_with_title(self):
        self.assert_html2rest(
            rest_string="""
                A inline |foo bar| image.

                .. |foo bar| image:: /url/to/image.png

                ...and some text below.
            """,
            html_string="""
                <p>A inline <img title="foo bar" src="/url/to/image.png" /> image.</p>
                <p>...and some text below.</p>
            """
        )

#    def test_preformat_unknown_nodes(self):
#        """
#        Put unknown tags in a <pre> area.
#        """
#        self.assert_html2rest(
#            rest_string=u"""
#                111 <<pre>><x><</pre>>foo<<pre>></x><</pre>> 222
#                333<<pre>><x foo1="bar1"><</pre>>foobar<<pre>></x><</pre>>444
#                
#                555<<pre>><x /><</pre>>666
#            """,
#            html_string="""
#                <p>111 <x>foo</x> 222<br />
#                333<x foo1="bar1">foobar</x>444</p>
#    
#                <p>555<x />666</p>
#            """,
#            emitter_kwargs={"unknown_emit":preformat_unknown_nodes}
#        )
#
#    def test_transparent_unknown_nodes(self):
#        """
#        transparent_unknown_nodes is the default unknown_emit:
#        
#        Remove all unknown html tags and show only
#        their child nodes' content.
#        """
#        self.assert_html2rest(
#            rest_string=u"""
#                111 <<pre>><x><</pre>>foo<<pre>></x><</pre>> 222
#                333<<pre>><x foo1="bar1"><</pre>>foobar<<pre>></x><</pre>>444
#                
#                555<<pre>><x /><</pre>>666
#            """,
#            html_string="""
#                <p>111 <x>foo</x> 222<br />
#                333<x foo1="bar1">foobar</x>444</p>
#    
#                <p>555<x />666</p>
#            """,
#        )


if __name__ == '__main__':
    unittest.main()
