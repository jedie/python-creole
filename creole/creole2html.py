# coding: utf-8

"""
    WikiCreole to HTML converter

    @copyright: 2007 MoinMoin:RadomirDopieralski,
                2008-2010 JensDiemer
    @license: GNU GPL v3 or above, see LICENSE for details.
"""

import sys, re, traceback

import default_macros
from creole_parser import Parser


#from PyLucid.tools.utils import escape
from xml.sax.saxutils import escape

class Rules:
    # For the link targets:
    proto = r'http|https|ftp|nntp|news|mailto|telnet|file|irc'
    extern = r'(?P<extern_addr>(?P<extern_proto>%s):.*)' % proto
    interwiki = r'''
            (?P<inter_wiki> [A-Z][a-zA-Z]+ ) :
            (?P<inter_page> .* )
        '''

class HtmlEmitter:
    """
    Generate HTML output for the document
    tree consisting of DocNodes.
    """

    addr_re = re.compile('|'.join([
            Rules.extern,
            Rules.interwiki,
        ]), re.X | re.U) # for addresses

    def __init__(self, root, macros=default_macros, verbose=1, stderr=sys.stderr):
        self.root = root
        self.macros = macros
        self.verbose = verbose
        self.stderr = stderr

    def get_text(self, node):
        """Try to emit whatever text is in the node."""
        try:
            return node.children[0].content or ''
        except:
            return node.content or ''

    def html_escape(self, text):
        return escape(text)
        #return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def attr_escape(self, text):
        return self.html_escape(text).replace('"', '&quot')

    # *_emit methods for emitting nodes of the document:

    def document_emit(self, node):
        return self.emit_children(node)

    def text_emit(self, node):
        return self.html_escape(node.content)

    def separator_emit(self, node):
        return u'<hr />\n\n'

    def paragraph_emit(self, node):
        return u'<p>%s</p>\n' % self.emit_children(node)

    def _list_emit(self, node, list_type):
        if node.parent.kind in ("document",):
            # The first list item
            formatter = u''
        else:
            formatter = u'\n'

        if list_type == "li":
            formatter += (
                u'%(i)s<%(t)s>%(c)s</%(t)s>'
            )
        else:
            formatter += (
                u'%(i)s<%(t)s>%(c)s\n'
                '%(i)s</%(t)s>'
            )
        return formatter % {
            "i": "\t" * node.level,
            "c": self.emit_children(node),
            "t": list_type,
        }

    def bullet_list_emit(self, node):
        return self._list_emit(node, list_type=u"ul")

    def number_list_emit(self, node):
        return self._list_emit(node, list_type=u"ol")

    def list_item_emit(self, node):
        return self._list_emit(node, list_type=u"li")

    def table_emit(self, node):
        return u'<table>\n%s</table>\n' % self.emit_children(node)

    def table_row_emit(self, node):
        return u'<tr>\n%s</tr>\n' % self.emit_children(node)

    def table_cell_emit(self, node):
        return u'\t<td>%s</td>\n' % self.emit_children(node)

    def table_head_emit(self, node):
        return u'\t<th>%s</th>\n' % self.emit_children(node)

    #--------------------------------------------------------------------------

    def _typeface(self, node, tag):
        return u'<%(tag)s>%(data)s</%(tag)s>' % {
            "tag": tag,
            "data": self.emit_children(node),
        }

    # TODO: How can we generalize that:
    def emphasis_emit(self, node):
        return self._typeface(node, tag="i")
    def strong_emit(self, node):
        return self._typeface(node, tag="strong")
    def monospace_emit(self, node):
        return self._typeface(node, tag="tt")
    def superscript_emit(self, node):
        return self._typeface(node, tag="sup")
    def subscript_emit(self, node):
        return self._typeface(node, tag="sub")
    def underline_emit(self, node):
        return self._typeface(node, tag="u")
    def small_emit(self, node):
        return self._typeface(node, tag="small")
    def delete_emit(self, node):
        return self._typeface(node, tag="del")

    #-------------------------------------------------------------------------- 

    def header_emit(self, node):
        return u'<h%d>%s</h%d>\n' % (
            node.level, self.html_escape(node.content), node.level)

    def preformatted_emit(self, node):
        return u'<pre>%s</pre>' % self.html_escape(node.content)

    def link_emit(self, node):
        target = node.content
        if node.children:
            inside = self.emit_children(node)
        else:
            inside = self.html_escape(target)
        m = self.addr_re.match(target)
        if m:
            if m.group('extern_addr'):
                return u'<a href="%s">%s</a>' % (
                    self.attr_escape(target), inside)
            elif m.group('inter_wiki'):
                raise NotImplementedError
        return u'<a href="%s">%s</a>' % (
            self.attr_escape(target), inside)

    def image_emit(self, node):
        target = node.content
        text = self.get_text(node)
        m = self.addr_re.match(target)
        if m and m.group('inter_wiki'):
            raise NotImplementedError

#            if m.group('extern_addr'):
#                return u'<img src="%s" alt="%s" />' % (
#                    self.attr_escape(target), self.attr_escape(text))
#                
#            elif 

        return u'<img src="%s" alt="%s" />' % (
            self.attr_escape(target), self.attr_escape(text))

    def macro_emit(self, node):
        #print node.debug()
        macro_name = node.macro_name
        macro = None

        if callable(self.macros):
            macro = lambda args, text: self.macros(macro_name, args=args, text=text)
        elif isinstance(self.macros, dict):
            try:
                macro = self.macros[macro_name]
            except KeyError, e:
                pass
        else:
            try:
                macro = getattr(self.macros, macro_name)
            except AttributeError, e:
                pass

        if macro == None:
            return self.error(
                u"Macro '%s' doesn't exist" % macro_name,
                handle_traceback=True
            )

        try:
            result = macro(args=node.macro_args, text=node.content)
        except Exception, err:
            return self.error(
                u"Macro '%s' error: %s" % (macro_name, err),
                handle_traceback=True
            )

        if not isinstance(result, unicode):
            msg = u"Macro '%s' doesn't return a unicode string!" % macro_name
            if self.verbose > 1:
                msg += " - returns: %r, type %r" % (result, type(result))
            return self.error(msg)

        if node.kind == "macro_block":
            result += "\n"

        return result
    macro_inline_emit = macro_emit
    macro_block_emit = macro_emit

    def break_emit(self, node):
        if node.parent.kind == "list_item":
            return u"<br />\n" + "\t" * node.parent.level
        elif node.parent.kind in ("table_head", "table_cell"):
            return u"<br />\n\t\t"
        else:
            return u"<br />\n"

    def line_emit(self, node):
        return u"\n"

    def pre_block_emit(self, node):
        """ pre block, with newline at the end """
        return u"<pre>%s</pre>\n" % self.html_escape(node.content)
    def pre_inline_emit(self, node):
        """ pre without newline at the end """
        return u"<pre>%s</pre>" % self.html_escape(node.content)

    def default_emit(self, node):
        """Fallback function for emitting unknown nodes."""
        raise NotImplementedError("Node '%s' unknown" % node.kind)

    def emit_children(self, node):
        """Emit all the children of a node."""
        return u''.join([self.emit_node(child) for child in node.children])

    def emit_node(self, node):
        """Emit a single node."""
        #print "%s_emit: %r" % (node.kind, node.content)
        emit = getattr(self, '%s_emit' % node.kind, self.default_emit)
        return emit(node)

    def emit(self):
        """Emit the document represented by self.root DOM tree."""
        return self.emit_node(self.root)

    def error(self, text, handle_traceback=False):
        """
        Error Handling.
        """
        if self.verbose > 1 and handle_traceback:
            self.stderr.write(
                "<pre>%s</pre>\n" % traceback.format_exc()
            )

        if self.verbose > 0:
            return u"[Error: %s]\n" % text
        else:
            # No error output
            return u""

if __name__ == "__main__":
    txt = u"""this is **bold** ok?
            for example ** this sentence"""

    print "-" * 80
#    from creole_alt.creole import Parser
    p = Parser(txt)
    document = p.parse()
    p.debug()

    html = HtmlEmitter(document).emit()
    print html
    print "-" * 79
    print html.replace(" ", ".").replace("\n", "\\n\n")
