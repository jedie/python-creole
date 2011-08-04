#!/usr/bin/env python
# coding: utf-8

"""
    html -> reStructuredText Emitter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Links about reStructuredText:
    
    http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html

    :copyleft: 2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import posixpath

from creole.shared.base_emitter import BaseEmitter
from creole.shared.markup_table import MarkupTable



class ReStructuredTextEmitter(BaseEmitter):
    """
    Build from a document_tree (html2creole.parser.HtmlParser instance) a
    creole markup text.
    """
    def __init__(self, *args, **kwargs):
        super(ReStructuredTextEmitter, self).__init__(*args, **kwargs)

        self.table_head_prefix = "_. "
        self.table_auto_width = False

        from creole.shared.unknown_tags import raise_unknown_node
        self._unknown_emit = raise_unknown_node
        self._block_data = []
        self._list_markup = ""

    def emit(self):
        """Emit the document represented by self.root DOM tree."""
        return self.emit_node(self.root).rstrip()

    #--------------------------------------------------------------------------

    def blockdata_pre_emit(self, node):
        """ pre block -> with newline at the end """
        pre_block = self.deentity.replace_all(node.content).strip()
        pre_block = "\n".join(["    %s" % line for line in pre_block.splitlines()])
        return "::\n\n%s\n\n" % pre_block

    def inlinedata_pre_emit(self, node):
        """ a pre inline block -> no newline at the end """
        return u"<pre>%s</pre>" % self.deentity.replace_all(node.content)

    def blockdata_pass_emit(self, node):
        return u"%s\n\n" % node.content
        return node.content

    #--------------------------------------------------------------------------

    def emit_children(self, node):
        """Emit all the children of a node."""

        result = u"".join(self.emit_children_list(node))

        if self._block_data and node.parent == self.root:
            # insert last bock data e.g.: .. |substitution| image:: /image.png
            result += "\n\n%s" % "\n".join(self._block_data)
            self._block_data = []

        return result

    def p_emit(self, node):
        return u"%s\n\n" % self.emit_children(node)

    HEADLINE_DATA = {
        1:("=", True),
        2:("-", True),
        3:("=", False),
        4:("-", False),
        5:('`', False),
        6:("'", False),
    }
    def headline_emit(self, node):
        text = self.emit_children(node)

        level = node.level
        if level > 6:
            level = 6

        char, both = self.HEADLINE_DATA[level]
        markup = char * len(text)

        if both:
            format = "%(m)s\n%(t)s\n%(m)s\n\n"
        else:
            format = "%(t)s\n%(m)s\n\n"

        return format % {"m":markup, "t":text}

    #--------------------------------------------------------------------------

    def _typeface(self, node, key):
        return key + self.emit_children(node) + key

    def strong_emit(self, node):
        return self._typeface(node, key="**")
    def b_emit(self, node):
        return self._typeface(node, key="**")
    big_emit = strong_emit

    def i_emit(self, node):
        return self._typeface(node, key="*")
    def em_emit(self, node):
        return self._typeface(node, key="*")

    def tt_emit(self, node):
        return self._typeface(node, key="``")

#    def sup_emit(self, node):
#        return self._typeface(node, key="^")
#    def sub_emit(self, node):
#        return self._typeface(node, key="~")
#    def del_emit(self, node):
#        return self._typeface(node, key="-")
#
#    def cite_emit(self, node):
#        return self._typeface(node, key="??")
#    def ins_emit(self, node):
#        return self._typeface(node, key="+")
#
#    def span_emit(self, node):
#        return self._typeface(node, key="%")
#    def code_emit(self, node):
#        return self._typeface(node, key="@")

    #--------------------------------------------------------------------------

#    def hr_emit(self, node):
#        return u"----\n\n"

    def a_emit(self, node):
        link_text = self.emit_children(node)
        url = node.attrs["href"]
        return u"`%s <%s>`_" % (link_text, url)

    def img_emit(self, node):
        src = node.attrs["src"]

        if src.split(':')[0] == 'data':
            return u""

        title = node.attrs.get("title", "")
        alt = node.attrs.get("alt", "")
        if len(alt) > len(title): # Use the longest one
            substitution_text = alt
        else:
            substitution_text = title

        if substitution_text == "": # Use filename as picture text
            substitution_text = posixpath.basename(src)

        self._block_data.append(
            u".. |%s| image:: %s" % (substitution_text, src)
        )

        return u"|%s|" % substitution_text

    #--------------------------------------------------------------------------

    def code_emit(self, node):
        return u"``%s``" % self._emit_content(node)

    #--------------------------------------------------------------------------

    def li_emit(self, node):
        content = self.emit_children(node).strip("\n")
        result = u"\n%s%s %s\n" % (
            "    " * (node.level - 1), self._list_markup, content
        )
        return result

    def _list_emit(self, node, list_type):
        self._list_markup = list_type
        content = self.emit_children(node)

        if node.level == 1:
            # FIXME: This should be made ​​easier and better
            complete_list = "\n\n".join([i.strip("\n") for i in content.split("\n") if i])
            content = "%s\n\n" % complete_list

        return content

    def ul_emit(self, node):
        return self._list_emit(node, "*")

    def ol_emit(self, node):
        return self._list_emit(node, "#.")

    def table_emit(self, node):
        """
        http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#tables
        """
        self._table = MarkupTable(
            head_prefix="",
            auto_width=True,
            debug_msg=self.debug_msg
        )
        self.emit_children(node)
        content = self._table.get_rest_table()
        return u"%s\n" % content








if __name__ == '__main__':
    import doctest
    print doctest.testmod()

#    import sys;sys.exit()
    from creole.html_parser.parser import HtmlParser

    data = u"""<p>A nested bullet lists:</p>
<ul>
<li><p>item 1</p>
<ul>
<li><p>A <strong>bold subitem 1.1</strong> here.</p>
<ul>
<li>subsubitem 1.1.1</li>
<li>subsubitem 1.1.2 with inline <img alt="substitution text" src="/url/to/image.png" /> image.</li>
</ul>
</li>
<li><p>subitem 1.2</p>
</li>
</ul>
</li>
<li><p>item 2</p>
<ul>
<li>subitem 2.1</li>
</ul>
</li>
</ul>
<p>Text under list.</p>
<p>4 <img alt="PNG pictures" src="/image.png" /> four</p>
<p>5 <img alt="Image without files ext?" src="/path1/path2/image" /> five</p>
"""

    print data
    h2c = HtmlParser(
#        debug=True
    )
    document_tree = h2c.feed(data)
    h2c.debug()

    e = ReStructuredTextEmitter(document_tree,
        debug=True
    )
    content = e.emit()
    print "*" * 79
    print content
    print "*" * 79
    print content.replace(" ", ".").replace("\n", "\\n\n")

