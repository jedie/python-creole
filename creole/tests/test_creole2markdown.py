from inspect import cleandoc

from creole.tests.utils.base_unittest import BaseCreoleTest


class Creole2MarkdownTests(BaseCreoleTest):
    def creole2markdown(self, creole_string, html_string, markdown_string, debug=False):
        self.assert_creole2html(raw_creole=creole_string, raw_html=html_string, debug=debug)
        self.assert_html2markdown(
            markdown_string=markdown_string,
            html_string=html_string,
        )

    def test_basic(self):
        self.creole2markdown(
            creole_string='= Headline =',
            html_string='<h1>Headline</h1>',
            markdown_string='# Headline',
            debug=True,
        )

    def test_newline(self):
        self.creole2markdown(
            creole_string=cleandoc(
                '''
                A Test line
                e.g.:
                {{{
                print('foobar')
                }}}
                Text below.
                '''
            ),
            html_string=cleandoc(
                '''
                <p>A Test line<br />
                e.g.:</p>
                <pre>
                print('foobar')
                </pre>
                <p>Text below.</p>
                '''
            ),
            markdown_string=cleandoc(
                '''
                A Test line
                e.g.:
                ```
                print('foobar')
                ```

                Text below.
                '''
            ),
            debug=True,
        )
