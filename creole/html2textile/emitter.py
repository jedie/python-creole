#!/usr/bin/env python
# coding: utf-8

"""
    html -> textile Emitter
    ~~~~~~~~~~~~~~~~~~~~~~


    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals
import posixpath

from creole.shared.base_emitter import BaseEmitter



class TextileEmitter(BaseEmitter):
    """
    Build from a document_tree (html2creole.parser.HtmlParser instance) a
    creole markup text.
    """

    def __init__(self, *args, **kwargs):
        super(TextileEmitter, self).__init__(*args, **kwargs)

        self.table_head_prefix = "_. "
        self.table_auto_width = False

    def emit(self):
        """Emit the document represented by self.root DOM tree."""
        return self.emit_node(self.root).strip() # FIXME

    #--------------------------------------------------------------------------

    def blockdata_pre_emit(self, node):
        """ pre block -> with newline at the end """
        return "<pre>%s</pre>\n" % self.deentity.replace_all(node.content)
    def inlinedata_pre_emit(self, node):
        """ a pre inline block -> no newline at the end """
        return "<pre>%s</pre>" % self.deentity.replace_all(node.content)

    def blockdata_pass_emit(self, node):
        return "%s\n\n" % node.content
        return node.content


    #--------------------------------------------------------------------------

    def p_emit(self, node):
        return "%s\n\n" % self.emit_children(node)

    def headline_emit(self, node):
        return "h%i. %s\n\n" % (node.level, self.emit_children(node))

    #--------------------------------------------------------------------------

    def _typeface(self, node, key):
        return key + self.emit_children(node) + key

    def strong_emit(self, node):
        return self._typeface(node, key="*")
    def b_emit(self, node):
        return self._typeface(node, key="**")
    big_emit = strong_emit

    def i_emit(self, node):
        return self._typeface(node, key="__")
    def em_emit(self, node):
        return self._typeface(node, key="_")

    def sup_emit(self, node):
        return self._typeface(node, key="^")
    def sub_emit(self, node):
        return self._typeface(node, key="~")
    def del_emit(self, node):
        return self._typeface(node, key="-")

    def cite_emit(self, node):
        return self._typeface(node, key="??")
    def ins_emit(self, node):
        return self._typeface(node, key="+")

    def span_emit(self, node):
        return self._typeface(node, key="%")
    def code_emit(self, node):
        return self._typeface(node, key="@")

    #--------------------------------------------------------------------------

    def hr_emit(self, node):
        return "----\n\n"

    def a_emit(self, node):
        link_text = self.emit_children(node)
        url = node.attrs["href"]
        return '"%s":%s' % (link_text, url)

    def img_emit(self, node):
        src = node.attrs["src"]

        if src.split(':')[0] == 'data':
            return ""

        title = node.attrs.get("title", "")
        alt = node.attrs.get("alt", "")
        if len(alt) > len(title): # Use the longest one
            text = alt
        else:
            text = title

        if text == "": # Use filename as picture text
            text = posixpath.basename(src)

        return "!%s(%s)!" % (src, text)

    #--------------------------------------------------------------------------

    def ul_emit(self, node):
        return self._list_emit(node, list_type="*")

    def ol_emit(self, node):
        return self._list_emit(node, list_type="#")








if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

#    import sys;sys.exit()
    from creole.html_parser.parser import HtmlParser

    data = """
<h1>Textile</h1>
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
"""

#    print(data.strip())
    h2c = HtmlParser(
        debug=True
    )
    document_tree = h2c.feed(data)
    h2c.debug()

    e = TextileEmitter(document_tree,
        debug=True
    )
    content = e.emit()
    print("*" * 79)
    print(content)
    print("*" * 79)
    print(content.replace(" ", ".").replace("\n", "\\n\n"))
