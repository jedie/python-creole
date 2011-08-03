#!/usr/bin/env python
# coding: utf-8

"""
    html -> reStructuredText Emitter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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

    def p_emit(self, node):
        result = u"%s\n\n" % self.emit_children(node)
        if self._block_data:
            result += u"%s\n\n" % "\n".join(self._block_data)
            self._block_data = []
        return result

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
        content = self.emit_children(node)
        return u"\n%s %s\n" % (self._inner_list, content)

    def ul_emit(self, node):
        return self._list_emit(node, list_type="-")

#    def ol_emit(self, node):
#        return self._list_emit(node, list_type="#")


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

    data = u"""
<p>Preformatting text:</p>
<pre>
Here some performatting
text... end.
</pre>
<p>Under pre block</p>
"""

    print data.strip()
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
