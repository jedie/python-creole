"""
    html -> Markdown Emitter
    ~~~~~~~~~~~~~~~~~~~~~~

    https://ct.de/y5hr

    :copyleft: 2021 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.

"""


import posixpath

from creole.parser.html_parser import HtmlParser
from creole.parser.html_parser_config import BLOCK_TAGS
from creole.shared.base_emitter import BaseEmitter
from creole.shared.document_tree import DocNode


class MarkdownEmitter(BaseEmitter):
    """
    Build from a document_tree (html2creole.parser.HtmlParser instance) a
    Markdown markup text.
    """

    def __init__(self, document_tree, strict=False, *args, **kwargs):
        self.strict = strict
        super().__init__(document_tree, *args, **kwargs)

        self.table_head_prefix = '= '
        self.table_auto_width = True

    def emit(self):
        """Emit the document represented by self.root DOM tree."""
        return self.emit_node(self.root).strip()  # FIXME

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
                    return f'```{language}{code}```\n\n'

            return f'```{code}```\n\n'

        return f'```{self.deentity.replace_all(pre_content)}```\n'

    def blockdata_pass_emit(self, node: DocNode):
        return f'{node.content}\n\n'

    # --------------------------------------------------------------------------

    def p_emit(self, node: DocNode):
        result = self.emit_children(node)
        if self._inner_list == '':
            result += '\n\n'
        return result

    def br_emit(self, node: DocNode):
        return '\n'

    def headline_emit(self, node: DocNode):
        prefix = '#' * node.level
        return f'{prefix} {self.emit_children(node)}\n\n'

    # --------------------------------------------------------------------------

    def strong_emit(self, node: DocNode):
        return self._typeface(node, key='**')

    b_emit = strong_emit
    big_emit = strong_emit

    def i_emit(self, node: DocNode):
        return self._typeface(node, key='_')

    def em_emit(self, node: DocNode):
        return self._typeface(node, key='*')

    def tt_emit(self, node: DocNode):
        return self._typeface(node, key='##')

    def sup_emit(self, node: DocNode):
        return self._typeface(node, key='^^')

    def sub_emit(self, node: DocNode):
        return self._typeface(node, key=',,')

    def u_emit(self, node: DocNode):
        return self._typeface(node, key='__')

    def small_emit(self, node: DocNode):
        return self._typeface(node, key='--')

    def del_emit(self, node: DocNode):
        return self._typeface(node, key='~~')

    strike_emit = del_emit

    # --------------------------------------------------------------------------

    def hr_emit(self, node: DocNode):
        return '----\n\n'

    def a_emit(self, node: DocNode):
        link_text = self.emit_children(node)
        url = node.attrs['href']
        title = node.attrs.get('title')
        if title:
            return f'[{link_text}]({url} "{title}")'
        else:
            return f'[{link_text}]({url})'

    def img_emit(self, node: DocNode):
        src = node.attrs['src']

        title = node.attrs.get('title')
        alt = node.attrs.get('alt', '')
        if title and alt:
            return f'![{alt}]({src} "{title}")'

        return f'![{alt}]({src})'

    # --------------------------------------------------------------------------

    def list_emit(self, node: DocNode):
        content = self.emit_children(node)
        if node.level == 1:
            content += '\n\n'
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
