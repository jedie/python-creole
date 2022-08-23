"""
    html -> Markdown Emitter
    ~~~~~~~~~~~~~~~~~~~~~~

    https://ct.de/y5hr

    :copyleft: 2021 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.

"""
from urllib.parse import ParseResult, quote, urlparse, urlunparse

from creole.parser.html_parser import HtmlParser
from creole.shared.base_emitter import BaseEmitter
from creole.shared.document_tree import DocNode
from creole.shared.markup_table import MarkupTable


def quote_link(uri):
    """
    >>> quote_link('http://foo.tld/a image with spaces.png')
    'http://foo.tld/a%20image%20with%20spaces.png'

    >>> quote_link('https://foo.tld/a image.png?bar=1#anchor')
    'https://foo.tld/a%20image.png?bar=1#anchor'
    """
    scheme, netloc, url, params, query, fragment = urlparse(uri)
    url = quote(url)
    return urlunparse(ParseResult(scheme, netloc, url, params, query, fragment))


class MarkdownEmitter(BaseEmitter):
    """
    Build from a document_tree (html2creole.parser.HtmlParser instance) a
    Markdown markup text.
    """

    def __init__(self, document_tree, strict=False, *args, **kwargs):
        self.strict = strict
        super().__init__(document_tree, *args, **kwargs)

    def emit(self):
        """Emit the document represented by self.root DOM tree."""
        return self.emit_node(self.root).strip()  # FIXME

    # --------------------------------------------------------------------------
    def table_emit(self, node):
        self._table = MarkupTable(head_prefix='', debug_msg=self.debug_msg)
        self.emit_children(node)
        content = self._table.get_markdown_table()
        return f'\n{content}\n'

    def tr_emit(self, node):
        self._table.add_tr()
        self.emit_children(node)
        return ''

    def th_emit(self, node):
        self._table.add_th(self.emit_children(node))
        return ''

    def td_emit(self, node):
        self._table.add_td(self.emit_children(node))
        return ''
    # --------------------------------------------------------------------------

    def blockdata_pre_emit(self, node: DocNode):
        """pre block -> with newline at the end"""
        return f'```{self.deentity.replace_all(node.content)}```\n'

    def inlinedata_pre_emit(self, node: DocNode):
        """a pre inline block -> no newline at the end"""
        pre_content = node.content

        if pre_content.endswith('</code>'):
            # TODO: The parser should parse this!
            p = HtmlParser(debug=True)
            root_node: DocNode = p.feed(pre_content, preprocess=False)
            code_node: DocNode = root_node.children[0]
            code = self.deentity.replace_all(code_node.children[0].content)

            class_value = code_node.attrs.get('class')
            if class_value:
                if class_value.startswith('language-'):
                    language = class_value.partition('-')[2]
                    return f'\n```{language}{code}```\n'

            return f'\n```{code}```\n'

        return f'\n```{self.deentity.replace_all(pre_content)}```\n'

    def blockdata_pass_emit(self, node: DocNode):
        return f'\n{node.content}\n'

    # --------------------------------------------------------------------------

    def p_emit(self, node: DocNode):
        return f'\n{self.emit_children(node)}\n'

    def br_emit(self, node: DocNode):
        return '\n'

    def headline_emit(self, node: DocNode):
        prefix = '#' * node.level
        if node.parent not in ('document', 'headline', 'p'):
            prefix = f'\n{prefix}'
        return f'{prefix} {self.emit_children(node)}\n'

    # --------------------------------------------------------------------------

    def strong_emit(self, node: DocNode):
        return self._typeface(node, key='**')

    b_emit = strong_emit
    big_emit = strong_emit

    def i_emit(self, node: DocNode):
        return self._typeface(node, key='_')

    em_emit = i_emit

    def tt_emit(self, node: DocNode):
        return self._typeface(node, key='##')

    def _typeface_html(self, node, tag):
        return f'<{tag}>{self.emit_children(node)}</{tag}>'

    def sup_emit(self, node: DocNode):
        return self._typeface_html(node, tag='sup')

    def sub_emit(self, node: DocNode):
        return self._typeface_html(node, tag='sub')

    def u_emit(self, node: DocNode):
        return self._typeface(node, key='__')

    def small_emit(self, node: DocNode):
        return self._typeface(node, key='--')

    def del_emit(self, node: DocNode):
        return self._typeface(node, key='~~')

    strike_emit = del_emit

    # --------------------------------------------------------------------------

    def hr_emit(self, node: DocNode):
        return '\n----\n'

    def a_emit(self, node: DocNode):
        link_text = self.emit_children(node)

        url = quote_link(node.attrs['href'])

        title = node.attrs.get('title')
        if title:
            return f'[{link_text}]({url} "{title}")'
        else:
            return f'[{link_text}]({url})'

    def img_emit(self, node: DocNode):
        src = quote_link(node.attrs['src'])

        title = node.attrs.get('title')
        alt = node.attrs.get('alt', '')
        if title and alt:
            return f'![{alt}]({src} "{title}")'

        return f'![{alt}]({src})'

    # --------------------------------------------------------------------------

    def list_emit(self, node: DocNode):
        content = self.emit_children(node)
        if node.level == 1:
            return f'\n{content}\n'
        return content

    ul_emit = list_emit
    ol_emit = list_emit

    def li_emit(self, node: DocNode):
        list_level = node.level

        list_node = node.parent
        list_kind = list_node.kind
        if list_kind == 'ul':
            prefix = '*'
        elif list_kind == 'ol':
            prefix = '1.'
        else:
            raise NotImplementedError(f'List type: {list_kind}')

        indent = '  ' * (list_level - 1)

        content = self.emit_children(node)
        return f"\n{indent}{prefix} {content}"

    # --------------------------------------------------------------------------
    def data_emit(self, node: DocNode):
        content = node.content
        if content == ' ':
            # FIXME: Because of bug in creole.html_tools.strip_html.strip_html()
            return ''
        return node.content

    def code_emit(self, node: DocNode):
        code_block = self._emit_content(node)
        assert '\n' not in code_block

        if '`' in code_block:
            return f'``{code_block}``'
        else:
            return f'`{code_block}`'

    # --------------------------------------------------------------------------

    def div_emit(self, node: DocNode):
        return self._emit_content(node)

    def span_emit(self, node: DocNode):
        return self._emit_content(node)
