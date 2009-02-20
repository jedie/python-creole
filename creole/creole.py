# -*- coding: iso-8859-1 -*-
"""
    Creole wiki markup parser

    See http://wikicreole.org/ for latest specs.

    Notes:
    * No markup allowed in headings.
      Creole 1.0 does not require us to support this.
    * No markup allowed in table headings.
      Creole 1.0 does not require us to support this.
    * No (non-bracketed) generic url recognition: this is "mission impossible"
      except if you want to risk lots of false positives. Only known protocols
      are recognized.
    * We do not allow ":" before "//" italic markup to avoid urls with
      unrecognized schemes (like wtf://server/path) triggering italic rendering
      for the rest of the paragraph.

    PyLucid Updates by the PyLucid team:
        - Bugfixes and better html code style
        - Make the image tag match more strict, so it doesn't clash with
            django template tags
        - Add a passthrough for all django template blocktags
        - Add a passthrough for html code lines

    @copyright: 2007 MoinMoin:RadomirDopieralski (creole 0.5 implementation),
                2007 MoinMoin:ThomasWaldmann (updates)
                2008 PyLucid:JensDiemer (PyLucid patches)
    @license: GNU GPL, see COPYING for details.
"""

import re






class InlineRules:
    """
    All inline rules
    """
    proto = r'http|https|ftp|nntp|news|mailto|telnet|file|irc'
    url =  r'''(?P<url>
            (^ | (?<=\s | [.,:;!?()/=]))
            (?P<escaped_url>~)?
            (?P<url_target> (?P<url_proto> %s ):\S+? )
            ($ | (?=\s | [,.:;!?()] (\s | $)))
        )''' % proto
    link = r'''(?P<link>
            \[\[
            (?P<link_target>.+?) \s*
            ([|] \s* (?P<link_text>.+?) \s*)?
            ]]
        )'''

#    link = r'''(?P<link1>
#            \[\[
#            (?P<link_target1>.+?)\|(?P<link_text1>.+?)
#            ]]
#        )|(?P<link2>
#            \[\[
#            (?P<link_target2> (%s)://[^ ]+) \s* (?P<link_text2>.+?)
#            ]]
#        )|
#            \[\[(?P<internal_link>.+)\]\]
#        ''' % proto

    #--------------------------------------------------------------------------
    # The image rule should not match on django template tags! So we make it
    # more restricted.
    # It matches only if...
    # ...image target ends with a picture extention
    # ...separator >|< and the image text exist
    image = r'''(?P<image>
            {{
            (?P<image_target>.+?(\.jpg|\.jpeg|\.gif|\.png)) \s*
            (\| \s* (?P<image_text>.+?) \s*)?
            }}
        )(?i)'''
    #--------------------------------------------------------------------------

    macro = r'''(?P<macro>
            <<(?P<macro_name> \w+) (?P<macro_args>.*?)>>
        )'''

    inline_macro = r'''
        (?P<inline_macro>
        << \s* (?P<inline_macro_start>\w+) \s* (?P<inline_macro_args>.*?) \s* >>
        (?P<inline_macro_text>(.|\n)*)
        <</ \s* (?P=inline_macro_start) \s* >>
        )
    '''
        
    preformatted = r'(?P<preformatted> {{{ (?P<preformatted_text>.*?) }}} )'
    
    # Basic text typefaces:
    emph = r'(?P<emph> (?<!:)// )' # there must be no : in front of the //
                                   # avoids italic rendering in urls with
                                   # unknown protocols
                                   
    strong = r'(?P<strong> \*\* )'
    
    # Creole 1.0 optional:
    monospace = r'(?P<monospace> \#\# )'
    superscript = r'(?P<superscript> \^\^ )'
    subscript = r'(?P<subscript> ,, )'
    underline = r'(?P<underline> __ )'
    delete = r'(?P<delete> ~~ )'
    
    # own additions:
    small = r'(?P<small> -- )'
    
    linebreak = r'(?P<linebreak> \\\\ )'
    escape = r'(?P<escape> ~ (?P<escaped_char>\S) )'
    char =  r'(?P<char> . )'

    pass_inline = r'''(?P<pass_inline>
            ({%.*?%})|
            ({{.*?}})
        )'''

    #--------------------------------------------------------------------------
    # Special rules




    
class BlockRules:
    """
    All used block rules.
    """
    # Pass-through all django template blocktags       
    pass_block = r'''
        (\n|\s)*?
        (?P<pass_block>
        \n{0,1}
        {% \s* (?P<pass_block_start>.+?) \s* (?P<pass_block_args>.*?) \s* %}
        (\n|.)*?
        {% \s* end(?P=pass_block_start) \s* %}
        \n{0,1}
        )
        (\n|\s)*?
    '''
    pass_line = r'''\n(?P<pass_line>
            \n
            ({%.*?%})|
            ({{.*?}})
            \n
        )\n\n'''
        
#    macro_block = r'''(?P<macro_block>
#            \s* << (?P<macro_block_start>\w+) \s* (?P<macro_block_args>.*?) >>
#            (?P<macro_block_text>(.|\n)+?)
#            <</(?P=macro_block_start)>> \s*
#        )'''
#    macro_block = r'''(?P<macro_block>
#            <<(?P<macro_block_start>.*?)>>
#            (?P<macro_block_text>.*?)
#            <</.*?>>
#        )'''

    macro_block = r'''
        (?P<macro_block>
        << \s* (?P<macro_block_start>\w+) \s* (?P<macro_block_args>.*?) \s* >>
        (?P<macro_block_text>(.|\n)*)
        <</ \s* (?P=macro_block_start) \s* >>
        )
    '''
    
    #Pass-through html code lines
    html = r'''(?P<html>
        ^[ \t]*<[a-zA-Z].*?<(/[a-zA-Z ]+?)>[ \t]*$
    )'''
        
    line = r'''(?P<line> ^\s*$ )''' # empty line that separates paragraphs
    
    head = r'''(?P<head>
        ^
        (?P<head_head>=+) \s*
        (?P<head_text> .*? )
        =*$
    )'''
    separator = r'(?P<separator> ^ \s* ---- \s* $ )' # horizontal line
    pre = r'''(?P<pre>
            ^{{{ \s* $
            (\n)?
            (?P<pre_text>
                ([\#]!(?P<pre_kind>\w*?)(\s+.*)?$)?
                (.|\n)+?
            )
            (\n)?
            ^}}} \s*$
        )'''
    list = r'''(?P<list>
        ^ [ \t]* ([*][^*\#]|[\#][^\#*]).* $
        ( \n[ \t]* [*\#]+.* $ )*
    )''' # Matches the whole list, separate items are parsed later. The
         # list *must* start with a single bullet.
         

    table = r'''^ \s*(?P<table>
            [|].*? \s*
            [|]?
        ) \s* $'''


    text = r'(?P<text> .+ ) (?P<break> (?<!\\)$\n(?!\s*$) )?'


class SpecialRules:
    """
    re rules witch not directly used as inline/block rules.
    """
    # Matches single list items:
    item = r'''^ \s* (?P<item>
        (?P<item_head> [\#*]+) \s*
        (?P<item_text> .*?)
    ) \s* $''' 
    
    # For splitting table cells:
    cell = r'''
            \| \s*
            (
                (?P<head> [=][^|]+ ) |
                (?P<cell> (  %s | [^|])+ )
            ) \s*
        ''' % '|'.join([
            InlineRules.link, InlineRules.macro, InlineRules.image,
            InlineRules.preformatted
        ])
        
    # For pre escaping, in creole 1.0 done with ~:
    pre_escape = r' ^(?P<indent>\s*) ~ (?P<rest> \}\}\} \s*) $'



BLOCK_FLAGS = re.VERBOSE | re.UNICODE | re.MULTILINE
BLOCK_RULES = (
    BlockRules.pass_block,
    BlockRules.pass_line,
    BlockRules.macro_block,
    BlockRules.html,
    BlockRules.line, BlockRules.head, BlockRules.separator, BlockRules.pre, BlockRules.list,
    BlockRules.table, BlockRules.text,
)

INLINE_FLAGS = re.VERBOSE | re.UNICODE
INLINE_RULES = (
    InlineRules.link, InlineRules.url,
    InlineRules.macro,
    InlineRules.inline_macro,
    InlineRules.preformatted, InlineRules.image,
    InlineRules.pass_inline,
    
    InlineRules.strong, InlineRules.emph,        
    InlineRules.monospace, InlineRules.underline,
    InlineRules.superscript, InlineRules.subscript,
    InlineRules.small, InlineRules.delete,

    InlineRules.linebreak,
    InlineRules.escape, InlineRules.char
)


def verify_rules(rules, flags):
    """
    Simple verify the rules -> try to compile it ;)
    """
    # Test with re.compile
    rule_list = []
    for rule in rules:
        try:
#            print rule
            re.compile(rule, flags)
        
            # Try to merge the rules. e.g. Check if group named double used.
            rule_list.append(rule)
            re.compile('|'.join(rule_list), flags)
        except Exception, err:
            print " *** Error with rule:"
            print rule
            print " -"*39            
            raise
    print "Rule test ok."


# If one rule failed, we can check this here.
# This schould be normaly off, only for debugging!
#verify_rules(INLINE_RULES, INLINE_FLAGS)
#verify_rules(BLOCK_RULES, BLOCK_FLAGS)





class Parser:
    """
    Parse the raw text and create a document object
    that can be converted into output using Emitter.
    """
    # For pre escaping, in creole 1.0 done with ~:
    pre_escape_re = re.compile(
        SpecialRules.pre_escape, re.MULTILINE | re.VERBOSE
    )
    
    # for link descriptions:
    link_re = re.compile(
        '|'.join([InlineRules.image, InlineRules.linebreak, InlineRules.char]),
        re.VERBOSE | re.UNICODE
    )
    # for list items:
    item_re = re.compile(
        SpecialRules.item, re.VERBOSE | re.UNICODE | re.MULTILINE
    )
    
    # for table cells:
    cell_re = re.compile(SpecialRules.cell, re.VERBOSE | re.UNICODE)
    
    # For block elements:
    block_re = re.compile('|'.join(BLOCK_RULES), BLOCK_FLAGS)
    
    # For inline elements:
    inline_re = re.compile('|'.join(INLINE_RULES), INLINE_FLAGS)

    def __init__(self, raw):
        self.raw = raw
        self.root = DocNode('document', None)
        self.cur = self.root        # The most recent document node
        self.text = None            # The node to add inline characters to
        self.last_text_break = None # Last break node, inserted by _text_repl()

    #--------------------------------------------------------------------------

    def cleanup_break(self, old_cur):
        """
        remove unused end line breaks.
        Should be called before a new block element.
        e.g.:
          <p>line one<br />
          line two<br />     <--- remove this br-tag
          </p>
        """
        if self.cur.children:
            last_child = self.cur.children[-1]
            if last_child.kind == "break":
                del(self.cur.children[-1])

    def _upto(self, node, kinds):
        """
        Look up the tree to the first occurence
        of one of the listed kinds of nodes or root.
        Start at the node node.
        """
        self.cleanup_break(node) # remove unused end line breaks.
        while node.parent is not None and not node.kind in kinds:
            node = node.parent
        
        return node

    def _upto_block(self):
        self.cur = self._upto(self.cur, ('document',))# 'section', 'blockquote'))

    #__________________________________________________________________________
    # The _*_repl methods called for matches in regexps. Sometimes the
    # same method needs several names, because of group names in regexps.

    def _pass_block_repl(self, groups):
        """ Pass-through all django template blocktags """          
        self._upto_block()
        self.cur = self.root
        DocNode("pass_block", self.cur, groups["pass_block"])
        self.text = None
    _pass_block_start_repl = _pass_block_repl
    _pass_block_end_repl = _pass_block_repl

    def _pass_line_repl(self, groups):
        """ Pass-through all django tags witch is alone in a code line """
        self._upto_block()
        self.cur = self.root
        DocNode("pass_line", self.cur, groups["pass_line"])
        self.text = None
        
    def _pass_inline_repl(self, groups):
        """ Pass-through all inline django tags"""
        DocNode("pass_inline", self.cur, groups["pass_inline"])
        self.text = None

    def _html_repl(self, groups):
        """ Pass-through html code """
        self._upto_block()
        DocNode("html", self.root, groups["html"])
        self.text = None

    def _text_repl(self, groups):
#        print "_text_repl()", self.cur.kind, groups.get('break') != None
        if self.cur.kind in ('table', 'table_row', 'bullet_list',
                                                                'number_list'):
            self._upto_block()

        if self.cur.kind in ('document', 'section', 'blockquote'):
            self.cur = DocNode('paragraph', self.cur)

        self.parse_inline(groups.get('text', u""))

        if groups.get('break') and self.cur.kind in ('paragraph',
            'emphasis', 'strong', 'preformatted'):
            self.last_text_break = DocNode('break', self.cur, u"")

        self.text = None
    _break_repl = _text_repl

    def _url_repl(self, groups):
        """Handle raw urls in text."""
        if not groups.get('escaped_url'):
            # this url is NOT escaped
            target = groups.get('url_target', u"")
            node = DocNode('link', self.cur)
            node.content = target
            DocNode('text', node, node.content)
            self.text = None
        else:
            # this url is escaped, we render it as text
            if self.text is None:
                self.text = DocNode('text', self.cur, u"")
            self.text.content += groups.get('url_target')
    _url_target_repl = _url_repl
    _url_proto_repl = _url_repl
    _escaped_url = _url_repl

    def _link_repl(self, groups):
        """Handle all kinds of links."""
        target = groups.get('link_target', u"")
        text = (groups.get('link_text', u"") or u"").strip()
        parent = self.cur
        self.cur = DocNode('link', self.cur)
        self.cur.content = target
        self.text = None
        re.sub(self.link_re, self._replace, text)
        self.cur = parent
        self.text = None
    _link_target_repl = _link_repl
    _link_text_repl = _link_repl

    def _add_macro(self, macro_name, macro_args, macro_text=u""):
#        self._upto_block()
        node = DocNode("macro", self.cur, macro_text.strip())
        node.macro_name = macro_name
        node.macro_args = macro_args.strip()
        self.text = None

    def _macro_block_repl(self, groups):
        """Handles macros using the placeholder syntax."""
        #self.debug_groups(groups)
        self._upto_block()
        self.cur = self.root
        self._add_macro(
            macro_name = groups['macro_block_start'],
            macro_text = groups.get('macro_block_text', u""),
            macro_args = groups.get('macro_block_args', u""),
        )
        self.text = None
    _macro_block_start_repl = _macro_block_repl
    _macro_block_args_repl = _macro_block_repl
    _macro_block_text_repl = _macro_block_repl

    def _macro_repl(self, groups):
        """Handles macros using the placeholder syntax."""
        macro_name = groups.get('macro_name', u"")
        macro_args = groups.get('macro_args', u"")
        self._add_macro(macro_name, macro_args)
        self.text = None

#        text = (groups.get('macro_text', u"") or u"").strip()
#        node = DocNode('macro', self.cur, name)
#        node.args = groups.get('macro_args', u"") or ''
#        DocNode('text', node, text or name)
#        self.text = None
    _macro_name_repl = _macro_repl
    _macro_args_repl = _macro_repl
#    _macro_text_repl = _macro_repl

    def _image_repl(self, groups):
        """Handles images and attachemnts included in the page."""
        target = groups.get('image_target', u"").strip()
        text = (groups.get('image_text', u"") or u"").strip()
        node = DocNode("image", self.cur, target)
        DocNode('text', node, text or node.content)
        self.text = None
    _image_target_repl = _image_repl
    _image_text_repl = _image_repl

    def _separator_repl(self, groups):
        self._upto_block()
        DocNode('separator', self.cur)

    def _item_repl(self, groups):
        bullet = groups.get('item_head', u"")
        text = groups.get('item_text', u"")
        if bullet[-1] == '#':
            kind = 'number_list'
        else:
            kind = 'bullet_list'
        level = len(bullet)-1
        lst = self.cur
        # Find a list of the same kind and level up the tree
        while (lst and
                   not (lst.kind in ('number_list', 'bullet_list') and
                        lst.level == level) and
                    not lst.kind in ('document', 'section', 'blockquote')):
            lst = lst.parent
        if lst and lst.kind == kind:
            self.cur = lst
        else:
            # Create a new level of list
            self.cur = self._upto(self.cur,
                ('list_item', 'document', 'section', 'blockquote'))
            self.cur = DocNode(kind, self.cur)
            self.cur.level = level
        self.cur = DocNode('list_item', self.cur)
        self.cur.level = level+1
        self.parse_inline(text)
        self.text = None
    _item_text_repl = _item_repl
    _item_head_repl = _item_repl

    def _list_repl(self, groups):
        self.item_re.sub(self._replace, groups["list"])

    def _head_repl(self, groups):
        self._upto_block()
        node = DocNode('header', self.cur, groups['head_text'].strip())
        node.level = len(groups['head_head'])
        self.text = None
    _head_head_repl = _head_repl
    _head_text_repl = _head_repl

    def _table_repl(self, groups):
        row = groups.get('table', '|').strip()
        self.cur = self._upto(self.cur, (
            'table', 'document', 'section', 'blockquote'))
        if self.cur.kind != 'table':
            self.cur = DocNode('table', self.cur)
        tb = self.cur
        tr = DocNode('table_row', tb)

        for m in self.cell_re.finditer(row):
            cell = m.group('cell')
            if cell:
                text = cell.strip()
                self.cur = DocNode('table_cell', tr)
                self.text = None
            else:
                text = m.group('head').strip('= ')
                self.cur = DocNode('table_head', tr)
                self.text = DocNode('text', self.cur, u"")
            self.parse_inline(text)

        self.cur = tb
        self.text = None

    def _pre_repl(self, groups):
        self._upto_block()
        kind = groups.get('pre_kind', None)
        text = groups.get('pre_text', u"")
        def remove_tilde(m):
            return m.group('indent') + m.group('rest')
        text = self.pre_escape_re.sub(remove_tilde, text)
        node = DocNode('preformatted', self.cur, text)
        node.sect = kind or ''
        self.text = None
    _pre_text_repl = _pre_repl
    _pre_head_repl = _pre_repl
    _pre_kind_repl = _pre_repl

    def _line_repl(self, groups):
        """ Transfer newline from the original markup into the html code """
        self._upto_block()
        DocNode('line', self.cur, u"")

    def _preformatted_repl(self, groups):
        text = groups.get('preformatted_text', u"")
        DocNode('preformatted', self.cur, text)
        self.text = None
    _preformatted_text_repl = _preformatted_repl
    _preformatted_head_repl = _preformatted_repl

    #--------------------------------------------------------------------------

    def _inline_mark(self, groups, key):
        if self.cur.kind != key:
            self.cur = DocNode(key, self.cur)
        else:
            self.cur = self._upto(self.cur, (key, )).parent
        self.text = None

    # TODO: How can we generalize that:
    def _emph_repl(self, groups):
        self._inline_mark(groups, key='emphasis')
    def _strong_repl(self, groups):
        self._inline_mark(groups, key='strong')
    def _monospace_repl(self, groups):
        self._inline_mark(groups, key='monospace')
    def _superscript_repl(self, groups):
        self._inline_mark(groups, key='superscript')
    def _subscript_repl(self, groups):
        self._inline_mark(groups, key='subscript')
    def _underline_repl(self, groups):
        self._inline_mark(groups, key='underline')
    def _small_repl(self, groups):
        self._inline_mark(groups, key='small')
    def _delete_repl(self, groups):
        self._inline_mark(groups, key='delete')

    #--------------------------------------------------------------------------

    def _linebreak_repl(self, groups):
        DocNode('break', self.cur, None)
        self.text = None

    def _escape_repl(self, groups):
        if self.text is None:
            self.text = DocNode('text', self.cur, u"")
        self.text.content += groups.get('escaped_char', u"")

    def _char_repl(self, groups):
        if self.text is None:
            self.text = DocNode('text', self.cur, u"")
        self.text.content += groups.get('char', u"")

    #--------------------------------------------------------------------------

    def _replace(self, match):
        """Invoke appropriate _*_repl method. Called for every matched group."""
        
        def debug(groups):
            from pprint import pformat
            data = dict([
                group for group in groups.iteritems() if group[1] is not None
            ])
            print "%s\n" % pformat(data)
        
        groups = match.groupdict()
        for name, text in groups.iteritems():
            if text is not None:
                #if name != "char": debug(groups)
                replace = getattr(self, '_%s_repl' % name)
                replace(groups)
                return

    def parse_inline(self, raw):
        """Recognize inline elements inside blocks."""
        re.sub(self.inline_re, self._replace, raw)

    def parse_block(self, raw):
        """Recognize block elements."""
        re.sub(self.block_re, self._replace, raw)

    def parse(self):
        """Parse the text given as self.raw and return DOM tree."""
        # convert all lineendings to \n
        text = self.raw.replace("\r\n", "\n").replace("\r", "\n")
        self.parse_block(text)
        return self.root


    #--------------------------------------------------------------------------
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
                print u"%s%s: %r" % (u" "*ident, child.kind, child.content)
                emit(child, ident+4)
        emit(start_node)
        print "*"*80

    def debug_groups(self, groups):
        print "_"*80
        print "  debug groups:"
        for name, text in groups.iteritems():
            if text is not None:
                print "%15s: %r" % (name, text)
        print "-"*80



#------------------------------------------------------------------------------


class DocNode:
    """
    A node in the document.
    """
    def __init__(self, kind='', parent=None, content=None):
        self.children = []
        self.parent = parent
        self.kind = kind

        if content:
            content = unicode(content)
        self.content = content

        if self.parent is not None:
            self.parent.children.append(self)

    def __str__(self):
#        return "DocNode kind '%s', content: %r" % (self.kind, self.content)
        return "<DocNode %s: %r>" % (self.kind, self.content)
    def __repr__(self):
        return u"<DocNode %s: %r>" % (self.kind, self.content)

#    def debug(self):
#        raise
#        print "_"*80
#        print "\tDocNode - debug:"
#        print "str(): %s" % self
#        print "attributes:"
#        for i in dir(self):
#            if i.startswith("_"):
#                continue
#            print "%20s: %r" % (i, getattr(self, i, "---"))


#------------------------------------------------------------------------------


if __name__=="__main__":
    import doctest
    doctest.testmod()
    print "doc test done."
    
    txt = r"""Creole **<<html>>&#x7B;...&#x7D;<</html>>** code"""
    txt = r"""foo
Y<<html>>the
code X<</html>>bar
Creole <<html>>&#x7B;...&#x7D;<</html>> code
 """

    print "-"*80
    p = Parser(txt)
    document = p.parse()
    p.debug()

    def display_match(match):
        groups = match.groupdict()
        for name, text in groups.iteritems():
            if name != "char" and text != None:
                print "%20s: %r" % (name, text)
    

    parser = Parser("")

    print "_"*80
    print "merged block rules test:"
    re.sub(parser.block_re, display_match, txt)
    
    print "_"*80
    print "merged inline rules test:"
    re.sub(parser.inline_re, display_match, txt)
    
    
    def test_single(rules, flags, txt):
        for rule in rules:
            rexp = re.compile(rule, flags)
            rexp.sub(display_match, txt)
            
    print "_"*80
    print "single block rules match test:"
    test_single(BLOCK_RULES, BLOCK_FLAGS, txt)
    
    print "_"*80
    print "single inline rules match test:"
    test_single(INLINE_RULES, INLINE_FLAGS, txt)
    

    print "---END---"