"""
    cross compare markdown unittest
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Compare all similarities between:
        * markdown2html (used the python markdown module)
        * html2markdown

    Note: This only works fine if there is no problematic whitespace handling.
        In this case, we must test in test_creole2html.py or test_html2creole.py

    :copyleft: 2021 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
from inspect import cleandoc

from creole.tests.utils.base_unittest import BaseCreoleTest


class CrossCompareMarkdownTests(BaseCreoleTest):
    def test_headline(self):
        self.cross_compare_markdown(
            markdown_string=cleandoc(
                '''
                # Headline

                Text under Headline

                ## Sub-Headline

                Text under Sub-Headline
                '''
            ),
            html_string=cleandoc(
                '''
                <h1>Headline</h1>
                <p>Text under Headline</p>
                <h2>Sub-Headline</h2>
                <p>Text under Sub-Headline</p>
            '''
            ),
            debug=True,
        )

    def test_links(self):
        self.cross_compare_markdown(
            markdown_string='[This is a Link](https//test.internal/foo/bar)',
            html_string='<p><a href="https//test.internal/foo/bar">This is a Link</a></p>',
        )
        self.cross_compare_markdown(
            markdown_string='[A Link](https//test.internal/ "Title")',
            html_string='<p><a href="https//test.internal/" title="Title">A Link</a></p>',
        )

    def test_images(self):
        self.cross_compare_markdown(
            markdown_string='![Alt text](/path/to/img.jpg)',
            html_string='<p><img alt="Alt text" src="/path/to/img.jpg" /></p>',
        )
        self.cross_compare_markdown(
            markdown_string='![Alt text](/path/to/img.jpg "Title")',
            html_string='<p><img alt="Alt text" src="/path/to/img.jpg" title="Title" /></p>',
        )

    def test_image_links(self):
        self.cross_compare_markdown(
            markdown_string='[![image](image.jpg)](/uri)',
            html_string='<p><a href="/uri"><img alt="image" src="image.jpg" /></a></p>',
        )
        self.cross_compare_markdown(
            markdown_string='[![image](image.jpg "Image Title")](/uri "Link Title")',
            html_string=(
                '<p><a href="/uri" title="Link Title">'
                '<img alt="image" src="image.jpg" title="Image Title" />'
                '</a></p>'
            ),
        )

    def test_hr(self):
        self.cross_compare_markdown(
            markdown_string='----',
            html_string='<hr />',
        )

    def test_typeface_basic(self):
        self.cross_compare_markdown(
            markdown_string='*single asterisks*',
            html_string='<p><em>single asterisks</em></p>',
        )
        self.cross_compare_markdown(
            markdown_string='**double asterisks**',
            html_string='<p><strong>double asterisks</strong></p>',
        )

    def test_inline_code(self):
        self.cross_compare_markdown(
            markdown_string='Use the `print()` function.',
            html_string='<p>Use the <code>print()</code> function.</p>',
            debug=True,
        )
        self.cross_compare_markdown(
            markdown_string='backtick in: ``print("`")`` function.',
            html_string='<p>backtick in: <code>print("`")</code> function.</p>',
            debug=True,
        )

        # self.cross_compare_markdown(
        #     markdown_string=cleandoc(
        #         '''
        #         This is: _italic_, **bold**, `monospace`.
        #         '''
        #     ),
        #     html_string=cleandoc(
        #         '''
        #         <p>This is: <em>italic</em>, <strong>bold</strong>, <code>monospace</code>.</p>
        #         '''
        #     ),
        #     debug=True,
        # )

    def test_lists(self):
        self.cross_compare_markdown(
            markdown_string=cleandoc(
                '''
                * apple
                * banana
                '''
            ),
            html_string=cleandoc(
                '''
                <ul>
                <li>apple</li>
                <li>banana</li>
                </ul>
                '''
            ),
        )
        self.cross_compare_markdown(
            markdown_string=cleandoc(
                '''
                1. apple
                1. banana
                '''
            ),
            html_string=cleandoc(
                '''
                <ol>
                <li>apple</li>
                <li>banana</li>
                </ol>
                '''
            ),
            debug=True,
        )
