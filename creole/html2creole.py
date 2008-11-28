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
pass_block_re = re.compile(
    r'''(?P<data>
        {% \s* (?P<pass_block_start>.+?) \s* .*? \s* %}
        (\n|.)*?
        {% \s* end(?P=pass_block_start) \s* %}
    )''',
    re.X | re.U | re.M
)

headline_tag_re = re.compile(r"h(\d)")



class DocNode:
    """
    A node in the document.
    """
    def __init__(self, kind='', parent=None, attrs=[], content=None, level=0):
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


class Html2CreoleEmitter(object):
    def __init__(self, document_tree, debug=False):
        self.root = document_tree
        self.debugging = debug
        self.__inner_list = None
        self.__mask_linebreak = False

    #-------------------------------------------------------------------------

    def data_emit(self, node):
        #~ node.debug()
        return node.content

    def blockdata_emit(self, node):
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
        if self.__mask_linebreak:
            return u"\\\\"
        else:
            return u"\n"

    def a_emit(self, node):
        node.debug()
        link_text = self.emit_children(node)
        return u"[[%s|%s]]" % (node.attrs["href"], link_text)

    def li_emit(self, node):
        self.__mask_linebreak = True
        result = u"%s %s\n" % (self.__inner_list*node.level, self.emit_children(node))
        self.__mask_linebreak = False
        return result

    def ul_emit(self, node):
        self.__inner_list = "*"
        return self.emit_children(node)

    def ol_emit(self, node):
        self.__inner_list = "#"
        return self.emit_children(node)

    #-------------------------------------------------------------------------

    def document_emit(self, node):
        return self.emit_children(node)

    def default_emit(self, node):
        """Fallback function for emitting unknown nodes."""
        msg = "Node '%s' unknown" % node.kind
        print msg
        #~ raise NotImplementedError(msg)

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
        emit_method = getattr(self, method_name, self.default_emit)
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
        return self.emit_node(self.root)

    #-------------------------------------------------------------------------

    def debug_msg(self, method, txt):
        if not self.debugging:
            return
        print "%13s: %s" % (method, txt)








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

    def _block_cut_out(self, match):
        data = match.group("data")
        self.blockdata.append(data)
        id = len(self.blockdata)-1
        return '<%s id="%s" />' % (self._placeholder, id)

    def feed(self, data):
        data = unicode(data)
        data = data.strip()
        data = re.sub(pass_block_re, self._block_cut_out, data)

        lines = data.split("\n")
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

        if tag in ("ul", "ol"):
            self.__list_level += 1

        if tag == "li":
            self.cur = DocNode(tag, self.cur, attrs, level=self.__list_level)
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
            DocNode(self._placeholder, self.cur, content = self.blockdata[id])
        #~ elif tag == "br":
            #~ self.cur = DocNode("br", self.cur)
        else:
            DocNode(tag, self.cur, attrs)

    def handle_endtag(self, tag):
        self.debug_msg("endtag", "%r" % tag)
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
                    txt += ": %s" % child.content
                if child.attrs:
                    txt += " (attrs: %r)" % child.attrs

                print txt
                emit(child, ident+4)
        emit(start_node)
        print "*"*80


data = """
<h1>Headline 1</h1>

<p>A text block, line 1<br />
and line 2</p>

<p><strong><i>bold italics</i></strong><br />
<i><strong>bold italics</strong></i><br />
<i>This is <strong>also</strong> good.</i></p>

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

<p>The current page name: &gt;{{ PAGE.name }}&lt; great?<br />
A {% lucidTag page_update_list count=10 %} PyLucid plugin</p>
{% block %}
FooBar
{% endblock %}
<p>A <a href="www.domain.tld">link</a>.<br />
no image: {{ foo|bar }}!</p>
"""

data = """
<h1>Headline 1</h1>

<p>A text block, line 1<br />
and line 2<br />
the end line 3</p>

<p>line 1: <strong><i>bold italics</i></strong><br />
line2: <i><strong>bold italics</strong></i><br />
line3: <i>This is <strong>also</strong> good.</i></p>
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
print e.emit()


