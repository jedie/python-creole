from creole.html2creole.unknown_tags import transparent_unknown_nodes
from creole.html2creole.deentity import Deentity
import posixpath
from creole.html2creole.config import BLOCK_TAGS
from creole.html2creole.parser import Html2CreoleParser


class Html2CreoleEmitter(object):

    def __init__(self, document_tree, unknown_emit=transparent_unknown_nodes, debug=False):
        self.root = document_tree

        self._unknown_emit = unknown_emit

        self.last = None
        self.debugging = debug

        self.deentity = Deentity() # for replacing html entities
        self.__inner_list = ""
        self.__mask_linebreak = False

    #--------------------------------------------------------------------------

    def blockdata_pre_emit(self, node):
        """ pre block -> with newline at the end """
        return u"{{{%s}}}\n" % self.deentity.replace_all(node.content)
    def inlinedata_pre_emit(self, node):
        """ a pre inline block -> no newline at the end """
        return u"{{{%s}}}" % self.deentity.replace_all(node.content)

    def blockdata_pass_emit(self, node):
        return u"%s\n\n" % node.content
        return node.content

    #--------------------------------------------------------------------------

    def data_emit(self, node):
        #node.debug()
        return node.content

    def entityref_emit(self, node):
        """
        emit a named html entity
        """
        entity = node.content

        try:
            return self.deentity.replace_named(entity)
        except KeyError, err:
            if self.debugging:
                print "unknown html entity found: %r" % entity
            return "&%s" % entity # FIXME
        except UnicodeDecodeError, err:
            raise UnicodeError(
                "Error handling entity %r: %s" % (entity, err)
            )

    def charref_emit(self, node):
        """
        emit a not named html entity
        """
        entity = node.content

        if entity.startswith("x"):
            # entity in hex
            hex_no = entity[1:]
            return self.deentity.replace_hex(hex_no)
        else:
            # entity as a unicode number
            return self.deentity.replace_number(entity)

    #--------------------------------------------------------------------------

    def p_emit(self, node):
        return u"%s\n\n" % self.emit_children(node)

    def br_emit(self, node):
        if self.__inner_list != "":
            return u"\\\\"
        else:
            return u"\n"

    def headline_emit(self, node):
        return u"%s %s\n\n" % (u"=" * node.level, self.emit_children(node))

    #--------------------------------------------------------------------------

    def _typeface(self, node, key):
        return key + self.emit_children(node) + key

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
        return u"----\n\n"

    def a_emit(self, node):
        link_text = self.emit_children(node)
        url = node.attrs["href"]
        if link_text == url:
            return u"[[%s]]" % url
        else:
            return u"[[%s|%s]]" % (url, link_text)

    def img_emit(self, node):
        src = node.attrs["src"]

        if src.split(':')[0] == 'data':
            return u""

        title = node.attrs.get("title", "")
        alt = node.attrs.get("alt", "")
        if len(alt) > len(title): # Use the longest one
            text = alt
        else:
            text = title

        if text == "": # Use filename as picture text
            text = posixpath.basename(src)

        return u"{{%s|%s}}" % (src, text)

    #--------------------------------------------------------------------------

    def li_emit(self, node):
        content = self.emit_children(node)
        return u"\n%s %s" % (self.__inner_list, content)

    def _list_emit(self, node, list_type):
        start_newline = False
        if self.last and self.last.kind not in BLOCK_TAGS:
            if not self.last.content or not self.last.content.endswith("\n"):
                start_newline = True

        if self.__inner_list == "": # Start a new list
            self.__inner_list = list_type
        else:
            start = False
            self.__inner_list += list_type

        content = u"%s" % self.emit_children(node)

        self.__inner_list = self.__inner_list[:-1]

        if self.__inner_list == "": # Start a new list
            if start_newline:
                return "\n" + content + "\n\n"
            else:
                return content.strip() + "\n\n"
        else:
            return content

    def ul_emit(self, node):
        return self._list_emit(node, list_type="*")

    def ol_emit(self, node):
        return self._list_emit(node, list_type="#")

    #--------------------------------------------------------------------------

    def table_emit(self, node):
        self._table = CreoleTable(self.debug_msg)
        self.emit_children(node)
        content = self._table.get_creole()
        return u"%s\n" % content

    def tr_emit(self, node):
        self._table.add_tr()
        content = self.emit_children(node)
        return u""

    def _escape_linebreaks(self, text):
        text = text.strip()
        text = text.split("\n")
        lines = [line.strip() for line in text]
        lines = [line for line in lines if line]
        content = "\\\\".join(lines)
        content = content.strip("\\")
        return content

    def th_emit(self, node):
        content = self.emit_children(node)
        content = self._escape_linebreaks(content)
        content = u"= %s" % content
        self._table.add_td(content)
        return u""

    def td_emit(self, node):
        content = self.emit_children(node)
        content = self._escape_linebreaks(content)
        self._table.add_td(content)
        return u""

    #--------------------------------------------------------------------------

    def _emit_content(self, node):
        content = self.emit_children(node)
        content = self._escape_linebreaks(content)
        if node.kind in BLOCK_TAGS:
            content = u"%s\n\n" % content
        return content

    def div_emit(self, node):
        return self._emit_content(node)

    def span_emit(self, node):
        return self._emit_content(node)

    #--------------------------------------------------------------------------

    def document_emit(self, node):
        self.last = node
        return self.emit_children(node)

    def emit_children(self, node):
        """Emit all the children of a node."""
        self.last = node
        result = []
        for child in node.children:
            content = self.emit_node(child)
            assert isinstance(content, unicode)
            result.append(content)
        return u"".join(result)
        #~ return u''.join([self.emit_node(child) for child in node.children])

    def emit_node(self, node):
        """Emit a single node."""
        self.debug_msg("emit_node", "%s: %r" % (node.kind, node.content))

        method_name = "%s_emit" % node.kind
        emit_method = getattr(self, method_name, None)

        if emit_method:
            content = emit_method(node)
        else:
            content = self._unknown_emit(self, node)

        if not isinstance(content, unicode):
            raise AssertionError(
                "Method '%s' returns no unicode (returns: %r)" % (
                    method_name, content
                )
            )
        self.last = node
        return content

    def emit(self):
        """Emit the document represented by self.root DOM tree."""
        result = self.emit_node(self.root)
        return result.strip() # FIXME

    #-------------------------------------------------------------------------

    def debug_msg(self, method, txt):
        if not self.debugging:
            return
        print "%13s: %s" % (method, txt)





class CreoleTable(object):
    """
    Container for holding table data and render the data in creole markup.
    Format every cell width to the same col width.
    
    >>> def debug_msg(*args): pass
    >>> t = CreoleTable(debug_msg)
    >>> t.add_tr()
    >>> t.add_td(u"= head1")
    >>> t.add_td(u"= head2")
    >>> t.add_tr()
    >>> t.add_td(u"1.1.")
    >>> t.add_td(u"1.2.")
    >>> t.add_tr()
    >>> t.add_td(u"2.1.")
    >>> t.add_td(u"2.2.")
    >>> t.get_creole().splitlines()
    [u'|= head1 |= head2 |', u'| 1.1.   | 1.2.   |', u'| 2.1.   | 2.2.   |']
    """
    def __init__(self, debug_msg):
        self.debug_msg = debug_msg
        self.rows = []
        self.row_index = None

    def add_tr(self):
        self.debug_msg("Table.add_tr", "")
        self.rows.append([])
        self.row_index = len(self.rows) - 1

    def add_td(self, text):
        if self.row_index == None:
            self.add_tr()

        self.debug_msg("Table.add_td", text)
        self.rows[self.row_index].append(text)

    def get_creole(self):
        """ return the table data in creole markup. """
        # preformat every table cell
        cells = []
        for row in self.rows:
            line_cells = []
            for cell in row:
                cell = cell.strip()
                if cell != "":
                    if cell.startswith("="):
                        cell += " " # Headline
                    else:
                        cell = " %s " % cell # normal cell
                line_cells.append(cell)
            cells.append(line_cells)

        # Build a list of max len for every column
        widths = [max(map(len, col)) for col in zip(*cells)]

        # Join every line with ljust
        lines = []
        for row in cells:
            cells = [cell.ljust(width) for cell, width in zip(row, widths)]
            lines.append("|" + "|".join(cells) + "|")

        result = "\n".join(lines)

        self.debug_msg("Table.get_creole", result)
        return result


if __name__ == '__main__':
    import doctest
    print doctest.testmod()

#    import sys;sys.exit()

    data = u"""
<b>foo</b> <ul><li>one</li></ul>

<b>foo2</b><ul><li>one2</li></ul>
"""

#    print data.strip()
    h2c = Html2CreoleParser(
        debug=True
    )
    document_tree = h2c.feed(data)
    h2c.debug()

    e = Html2CreoleEmitter(document_tree,
        debug=True
    )
    content = e.emit()
    print "*" * 79
    print content
    print "*" * 79
    print content.replace(" ", ".").replace("\n", "\\n\n")
