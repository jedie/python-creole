from inspect import cleandoc

from creole.tests.utils.base_unittest import BaseCreoleTest


class MarkdownTests(BaseCreoleTest):
    def test_code_block(self):
        self.assert_html2markdown(
            markdown_string=cleandoc(
                '''
                Two prints:

                ```python
                print(1)
                print(2)
                ```

                Below the code block.
                '''
            ),
            html_string=cleandoc(
                '''
                <p>Two prints:</p>
                <pre><code class="language-python">
                print(1)
                print(2)
                </code></pre>
                <p>Below the code block.</p>
                '''
            ),
            # debug=True,
        )

    def test_lists(self):
        self.assert_html2markdown(
            markdown_string=cleandoc(
                '''
                * one
                  * one-one
                  * one-two
                * two
                  1. two-one
                  1. two-two
                '''
            ),
            html_string=cleandoc(
                '''
                <ul>
                    <li>one
                        <ul>
                            <li>one-one</li>
                            <li>one-two</li>
                        </ul>
                    </li>
                    <li>two
                        <ol>
                            <li>two-one</li>
                            <li>two-two</li>
                        </ol>
                    </li>
                </ul>
                '''
            ),
        )
        self.assert_html2markdown(
            markdown_string=cleandoc(
                '''
                * "one" and "two"
                * "three"
                '''
            ),
            html_string=cleandoc(
                '''
                <ul>
                <li>&quot;one&quot; and &quot;two&quot;</li>
                <li>&quot;three&quot;</li>
                </ul>
                '''
            ),
            # debug=True,
        )
        self.assert_html2markdown(
            markdown_string=cleandoc(
                '''
                * html2markdown

                Here the `--help` output
                '''
            ),
            html_string=cleandoc(
                '''
                <ul>
                    <li>html2markdown</li>
                </ul>
                <p>Here the <code>--help</code> output</p>
                '''
            ),
            # debug=True,
        )

    def test_table(self):
        self.assert_html2markdown(
            markdown_string=cleandoc(
                '''
                | A1 | B1 |
                | A2 | B2 |
                '''
            ),
            html_string=cleandoc(
                '''
                <table>
                <tr><td>A1</td><td>B1</td></tr>
                <tr><td>A2</td><td>B2</td></tr>
                </table>
                '''
            ),
            # debug=True,
        )
        self.assert_html2markdown(
            markdown_string=cleandoc(
                '''
                # A Table

                | Foo | Bar |
                | --- | --- |
                | A1  | B1  |
                | A2  | B2  |

                Text after the table.
                '''
            ),
            html_string=cleandoc(
                '''
                <h1>A Table</h1>
                <table>
                <tr><th>Foo</th><th>Bar</th></tr>
                <tr><td>A1</td><td>B1</td></tr>
                <tr><td>A2</td><td>B2</td></tr>
                </table>
                <p>Text after the table.</p>
                '''
            ),
            debug=True,
        )
        self.assert_html2markdown(
            markdown_string=cleandoc(
                '''
                A table:

                | A1 | B1 |

                Text after.
                '''
            ),
            html_string=cleandoc(
                '''
                <p>A table:</p>
                <table>
                <tr><td>A1</td><td>B1</td></tr>
                </table>
                <p>Text after.</p>
                '''
            ),
            # debug=True,
        )
