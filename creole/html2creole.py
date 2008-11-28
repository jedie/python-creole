# -*- coding: utf-8 -*-

import re
import inspect
from pprint import pprint
from HTMLParser import HTMLParser


BLOCK_TAGS = (
    "address", "blockquote", "center", "del", "dir", "div", "dl", "fieldset",
    "form",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "hr", "ins", "isindex", "menu", "noframes", "noscript",
    "ul", "ol", "table",
    "p", "pre"
)

# Pass-through all django template blocktags
pass_block_re = r'''(?P<pass_block>
    {% \s* (?P<pass_block_start>.+?) \s* .*? \s* %}
    (\n|.)*?
    {% \s* end(?P=pass_block_start) \s* %}
)'''
pre_block_re = r'''
    <pre>
    (?P<pre_block>
        (\n|.)*?
    )
    </pre>
'''
tt_block_re = r'''
    <tt>
    (?P<tt_block>
        (\n|.)*?
    )
    </tt>
'''

block_re = re.compile(
    '|'.join([
        pass_block_re,
        pre_block_re,
        tt_block_re,
    ]),
    re.X | re.U | re.M
)

headline_tag_re = re.compile(r"h(\d)")



class DocNode:
    """
    A node in the document.
    """
    def __init__(self, kind='', parent=None, attrs=[], content=None, level=None):
        self.kind = kind

        self.children = []
        self.parent = parent
        if self.parent is not None:
            self.parent.children.append(self)

        self.attrs = dict(attrs)
        self.content = content
        self.level = level

    def __str__(self):
#        return "DocNode kind '%s', content: %r" % (self.kind, self.content)
        return "<DocNode %s: %r>" % (self.kind, self.content)
    def __repr__(self):
        return u"<DocNode %s: %r>" % (self.kind, self.content)

    def debug(self):
        print "_"*80
        print "\tDocNode - debug:"
        print "str(): %s" % self
        print "attributes:"
        for i in dir(self):
            if i.startswith("_") or i == "debug":
                continue
            print "%20s: %r" % (i, getattr(self, i, "---"))


class DebugList(list):
    def __init__(self, html2creole):
        self.html2creole = html2creole
        super(DebugList, self).__init__()

    def append(self, item):
#        for stack_frame in inspect.stack(): print stack_frame

        line, method = inspect.stack()[1][2:4]

        print "%-8s   append: %-35r (%-15s line:%s)" % (
            self.html2creole.getpos(), item,
            method, line
        )
        list.append(self, item)






class Html2CreoleParser(HTMLParser):
    _placeholder = "blockdata"

    def __init__(self, debug=False):
        HTMLParser.__init__(self)

        self.debugging = debug
        if self.debugging:
            print "_"*79
            print "Html2Creole debug is on! print every data append."
            self.result = DebugList(self)
        else:
            self.result = []

        self.blockdata = []

        self.root = DocNode("document", None)
        self.cur = self.root

        self.__list_level = 0

    def _pre_cut(self, data, type):
        self.blockdata.append(data)
        id = len(self.blockdata)-1
        return '<%s type="%s" id="%s" />' % (self._placeholder, type, id)

    def _pre_tt_block_cut(self, groups):
        return self._pre_cut(groups["tt_block"], "tt")
    
    def _pre_pre_block_cut(self, groups):
        return self._pre_cut(groups["pre_block"], "pre")
    
    def _pre_pass_block_cut(self, groups):
        return self._pre_cut(groups["pass_block"], "pass")
    
    _pre_pass_block_start_cut = _pre_pass_block_cut
        
    def _pre_cut_out(self, match):        
        groups = match.groupdict()
        for name, text in groups.iteritems():
            if text is not None:
                #if name != "char": print "%15s: %r" % (name, text)
                print "%15s: %r" % (name, text)
                method = getattr(self, '_pre_%s_cut' % name)
                return method(groups)
        
#        data = match.group("data")


    def feed(self, data):
        data = unicode(data)
        data = data.strip()
        data = re.sub(block_re, self._pre_cut_out, data)

        lines = data.split("\n") # FIXME: linebreaks in list!
        lines = [l.strip() for l in lines]
        lines = [l for l in lines if l]

        clean_data = u" "
        for line in lines:
            if line and clean_data[-1] == u">" and line[0] == u"<":
                clean_data += line
                continue

            clean_data += " " + line

        clean_data = clean_data.strip()

        HTMLParser.feed(self, clean_data)

        return self.root


    #-------------------------------------------------------------------------

    def _upto(self, node, kinds):
        """
        Look up the tree to the first occurence
        of one of the listed kinds of nodes or root.
        Start at the node node.
        """
        while node.parent is not None:
            node = node.parent
            if node.kind in kinds:
                break

        return node

    def _go_up(self):
        kinds = list(BLOCK_TAGS) + ["document"]
        self.cur = self._upto(self.cur, kinds)

    #-------------------------------------------------------------------------

    def handle_starttag(self, tag, attrs):
        self.debug_msg("starttag", "%r atts: %s" % (tag, attrs))

        headline = headline_tag_re.match(tag)
        if headline:
            self.cur = DocNode(
                "headline", self.cur, level = int(headline.group(1))
            )
            return

        if tag in ("li", "ul", "ol"):
            self.cur = DocNode(tag, self.cur, attrs, level=self.__list_level)
            if tag in ("ul", "ol"):
                self.__list_level += 1
            return

        self.cur = DocNode(tag, self.cur, attrs)

    def handle_data(self, data):
        self.debug_msg("data", "%r" % data)
        DocNode("data", self.cur, content = data)

    def handle_charref(self, name):
        self.debug_msg("charref", "%r" % name)

    def handle_entityref(self, name):
        self.debug_msg("entityref", "%r" % name)

    def handle_startendtag(self, tag, attrs):
        self.debug_msg("startendtag", "%r atts: %s" % (tag, attrs))
        attr_dict = dict(attrs)
        if tag == self._placeholder:
            id = int(attr_dict["id"])
#            block_type = attr_dict["type"]
            DocNode(
                "%s_%s" % (self._placeholder, attr_dict["type"]),
                self.cur,
                content = self.blockdata[id],
#                attrs = attr_dict
            )
        else:
            DocNode(tag, self.cur, attrs)

    def handle_endtag(self, tag):
        self.debug_msg("endtag", "%r" % tag)
        
        if tag in ("ul", "ol"):
            self.__list_level -= 1
            
        if tag in BLOCK_TAGS:
            self._go_up()
        else:
            self.cur = self.cur.parent

    #-------------------------------------------------------------------------

    def debug_msg(self, method, txt):
        if not self.debugging:
            return
        print "%-8s %8s: %s" % (self.getpos(), method, txt)

    def debug(self, start_node=None):
        """
        Display the current document tree
        """
        print "_"*80

        if start_node == None:
            start_node = self.root
            print "  document tree:"
        else:
            print "  tree from %s:" % start_node

        print "="*80
        def emit(node, ident=0):
            for child in node.children:
                txt = u"%s%s" % (u" "*ident, child.kind)

                if child.content:
                    txt += ": %r" % child.content
                    
                if child.attrs:
                    txt += " - attrs: %r" % child.attrs
                    
                if child.level != None:
                    txt += " - level: %r" % child.level

                print txt
                emit(child, ident+4)
        emit(start_node)
        print "*"*80















class Html2CreoleEmitter(object):
    def __init__(self, document_tree, debug=False):
        self.root = document_tree
        self.debugging = debug
        self.__inner_list = None
        self.__mask_linebreak = False

    #--------------------------------------------------------------------------
    
    def _escape_linebreaks(self, text):
        text = text.split("\n")
        lines = [line.strip() for line in text]
        return "\\\\".join(lines)
    
    #--------------------------------------------------------------------------
    
    def blockdata_pre_emit(self, node):
        return u"{{{%s}}}\n" % node.content
    
    def blockdata_tt_emit(self, node):
        return u"{{{ %s }}}" % node.content
    
    def blockdata_pass_emit(self, node):
        return node.content
    
    #--------------------------------------------------------------------------

    def data_emit(self, node):
        #~ node.debug()
        return node.content

    def headline_emit(self, node):
        return u"%s %s\n\n" % (u"="*node.level, self.emit_children(node))

    def p_emit(self, node):
        #~ node.debug()
        return u"%s\n\n" % self.emit_children(node)

    def strong_emit(self, node):
        return u"**%s**" % self.emit_children(node)

    def i_emit(self, node):
        return u"//%s//" % self.emit_children(node)

    def br_emit(self, node):
        return u"\n"

    def hr_emit(self, node):
        return u"----\n"

    def a_emit(self, node):
        link_text = self.emit_children(node)
        return u"[[%s|%s]]" % (node.attrs["href"], link_text)
    
    def img_emit(self, node):
        node.debug()
        return u"{{%(src)s|%(alt)s}}" % node.attrs

    #--------------------------------------------------------------------------

    def li_emit(self, node):      
        content = self.emit_children(node)
        print "XXX", repr(content)
        content = self._escape_linebreaks(content)
        list_markup = self.__inner_list*node.level
        return u"%s %s\n" % (list_markup, content)

    def ul_emit(self, node):
        self.__inner_list = "*"
        content = self.emit_children(node)
        if node.level == 0:
            return u"%s\n" % content
        else:
            return u"%s" % content

    def ol_emit(self, node):
        self.__inner_list = "#"
        return u"%s\n" % self.emit_children(node)

    #--------------------------------------------------------------------------
    
    def table_emit(self, node):
        table_content = self.emit_children(node)
        
        # Optimize the table output
        lines = table_content.split("\n")      
        len_info = {}
        for line in lines:
            cells = line.split("|")
            for no, cell in enumerate(cells):
                cell_len = len(cell)
                if no not in len_info:
                    len_info[no] = cell_len
                elif len_info[no]<cell_len:
                    len_info[no] = cell_len
      
        new_lines = []
        for line in lines:
            cells = line.split("|")
            for no, cell in enumerate(cells):
                cells[no] = cell.ljust(len_info[no]+1) 
        
            new_lines.append("|".join(cells).strip())

        return "\n".join(new_lines)
    
    def tr_emit(self, node):
        return "%s|\n" % self.emit_children(node)
    
    def th_emit(self, node):
        content = self.emit_children(node)
        content = self._escape_linebreaks(content)
        return u"|= %s" % content
    
    def td_emit(self, node):
        content = self.emit_children(node)
        content = self._escape_linebreaks(content)
        return u"| %s" % content
    
    #--------------------------------------------------------------------------

    def document_emit(self, node):
        return self.emit_children(node)

#    def default_emit(self, node):
#        """Fallback function for emit unknown nodes."""
#        msg = "Node '%s' unknown!" % node.kind
#        print msg
#        raise NotImplementedError(msg)

    def emit_children(self, node):
        """Emit all the children of a node."""
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
        print "method name:", method_name
        emit_method = getattr(self, method_name)#, self.default_emit)
        content = emit_method(node)
        if not isinstance(content, unicode):
            raise AssertionError(
                "Method '%s' returns no unicode (returns: %r)" % (
                    method_name, content
                )
            )
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






if __name__ == '__main__':
    data = """
<h4>List a:</h4>
<ul>
    <li>a1 item</li>
    <ul>
        <li>a1.1 Force
        linebreak</li>
        <li>a1.2 item</li>
        <ul>
            <li>a1.2.1 item</li>
            <li>a1.2.2 item</li>
        </ul>
    </ul>
    <li>a2 item</li>
</ul>
<p>list 'a' end</p>
"""

    print data.strip()
    h2c = Html2CreoleParser(
        #~ debug=False
        debug=True
    )
    document_tree = h2c.feed(data)
    h2c.debug()
    
    e = Html2CreoleEmitter(document_tree,
        #~ debug=False
        debug=True
    )
    content = e.emit()
    print "*"*79
    print content 
    print "*"*79


