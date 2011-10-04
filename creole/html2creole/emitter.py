#!/usr/bin/env python
# coding: utf-8

"""
    html -> creole Emitter
    ~~~~~~~~~~~~~~~~~~~~~~


    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals
import posixpath

from creole.shared.base_emitter import BaseEmitter



class CreoleEmitter(BaseEmitter):
    """
    Build from a document_tree (html2creole.parser.HtmlParser instance) a
    creole markup text.
    """
    def __init__(self, *args, **kwargs):
        super(CreoleEmitter, self).__init__(*args, **kwargs)

        self.table_head_prefix = "= "
        self.table_auto_width = True

    def emit(self):
        """Emit the document represented by self.root DOM tree."""
        return self.emit_node(self.root).strip() # FIXME

    #--------------------------------------------------------------------------

    def blockdata_pre_emit(self, node):
        """ pre block -> with newline at the end """
        return "{{{%s}}}\n" % self.deentity.replace_all(node.content)
    def inlinedata_pre_emit(self, node):
        """ a pre inline block -> no newline at the end """
        return "{{{%s}}}" % self.deentity.replace_all(node.content)

    def blockdata_pass_emit(self, node):
        return "%s\n\n" % node.content
        return node.content

    #--------------------------------------------------------------------------

    def p_emit(self, node):
        result = self.emit_children(node)
        if self._inner_list == "":
            result += "\n\n"
        return result

    def br_emit(self, node):
        if self._inner_list != "":
            return "\\\\"
        else:
            return "\n"

    def headline_emit(self, node):
        return "%s %s\n\n" % ("=" * node.level, self.emit_children(node))

    #--------------------------------------------------------------------------

    def strong_emit(self, node):
        return self._typeface(node, key="**")
    b_emit = strong_emit
    big_emit = strong_emit

    def i_emit(self, node):
        return self._typeface(node, key="//")
    em_emit = i_emit

    def tt_emit(self, node):
        return self._typeface(node, key="##")
    def sup_emit(self, node):
        return self._typeface(node, key="^^")
    def sub_emit(self, node):
        return self._typeface(node, key=",,")
    def u_emit(self, node):
        return self._typeface(node, key="__")
    def small_emit(self, node):
        return self._typeface(node, key="--")
    def del_emit(self, node):
        return self._typeface(node, key="~~")
    strike_emit = del_emit

    #--------------------------------------------------------------------------

    def hr_emit(self, node):
        return "----\n\n"

    def a_emit(self, node):
        link_text = self.emit_children(node)
        try:
            url = node.attrs["href"]
        except KeyError:
            # e.g.: <a name="anchor-one">foo</a>
            return link_text
        if link_text == url:
            return "[[%s]]" % url
        else:
            return "[[%s|%s]]" % (url, link_text)

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

        return "{{%s|%s}}" % (src, text)

    #--------------------------------------------------------------------------

    def ul_emit(self, node):
        return self._list_emit(node, list_type="*")

    def ol_emit(self, node):
        return self._list_emit(node, list_type="#")

    #--------------------------------------------------------------------------

    def div_emit(self, node):
        return self._emit_content(node)

    def span_emit(self, node):
        return self._emit_content(node)






if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

#    import sys;sys.exit()
    from creole.html_parser.parser import HtmlParser

    data = """A <<test_macro1 args="foo1">>bar1<</test_macro1>> in a line..."""

#    print(data.strip())
    h2c = HtmlParser(
        debug=True
    )
    document_tree = h2c.feed(data)
    h2c.debug()

    from creole.shared.unknown_tags import escape_unknown_nodes

    e = CreoleEmitter(document_tree,
        debug=True,
        unknown_emit=escape_unknown_nodes
    )
    content = e.emit()
    print("*" * 79)
    print(content)
    print("*" * 79)
    print(content.replace(" ", ".").replace("\n", "\\n\n"))
