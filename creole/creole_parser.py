# coding: utf-8

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


    @copyright: 2007 MoinMoin:RadomirDopieralski (creole 0.5 implementation),
                2007 MoinMoin:ThomasWaldmann (updates)
                2008-2010 JensDiemer
    @license: GNU GPL v3 or above, see LICENSE for details.
"""

import re






class InlineRules:
    """
    All inline rules
    """
    proto = r'http|https|ftp|nntp|news|mailto|telnet|file|irc'
    url = r'''(?P<url>
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

    # image tag
    image = r'''(?P<image>
            {{
            (?P<image_target>.+?) \s*
            (\| \s* (?P<image_text>.+?) \s*)?
            }}
        )(?i)'''
    #--------------------------------------------------------------------------

    # a macro like: <<macro>>text<</macro>>
    inline_macro = r'''
        (?P<inline_macro>
        << \s* (?P<macro_inline_start>\w+) \s* (?P<macro_inline_args>.*?) \s* >>
        (?P<macro_inline_text>(.|\n)*?)
        <</ \s* (?P=macro_inline_start) \s* >>
        )
    '''
    # A single macro tag, like <<macro-a foo="bar">> or <<macro />>
    macro_tag = r'''(?P<macro_tag>
            <<(?P<macro_tag_name> \w+) (?P<macro_tag_args>.*?) \s* /*>>
        )'''

    pre_inline = r'(?P<pre_inline> {{{ (?P<pre_inline_text>.*?) }}} )'

    # Basic text typefaces:

    emphasis = r'(?P<emphasis>(?<!:)// (?P<emphasis_text>.+?) (?<!:)// )'
    # there must be no : in front of the // avoids italic rendering
    # in urls with unknown protocols

    strong = r'(?P<strong>\*\* (?P<strong_text>.+?) \*\* )'

    # Creole 1.0 optional:
    monospace = r'(?P<monospace> \#\# (?P<monospace_text>.+?) \#\# )'
    superscript = r'(?P<superscript> \^\^ (?P<superscript_text>.+?) \^\^ )'
    subscript = r'(?P<subscript> ,, (?P<subscript_text>.+?) ,, )'
    underline = r'(?P<underline> __ (?P<underline_text>.+?) __ )'
    delete = r'(?P<delete> ~~ (?P<delete_text>.+?) ~~ )'

    # own additions:
    small = r'(?P<small>-- (?P<small_text>.+?) -- )'

    linebreak = r'(?P<linebreak> \\\\ )'
    escape = r'(?P<escape> ~ (?P<escaped_char>\S) )'
    char = r'(?P<char> . )'






class BlockRules:
    """
    All used block rules.
    """
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
        (?P<macro_block_text>(.|\n)*?)
        <</ \s* (?P=macro_block_start) \s* >>
        )
    '''

    line = r'''(?P<line> ^\s*$ )''' # empty line that separates paragraphs

    head = r'''(?P<head>
        ^
        (?P<head_head>=+) \s*
        (?P<head_text> .*? )
        =*$
    )'''
    separator = r'(?P<separator> ^ \s* ---- \s* $ )' # horizontal line

    pre_block = r'''(?P<pre_block>
            ^{{{ \s* $
            (?P<pre_block_text>
                ([\#]!(?P<pre_block_kind>\w*?)(\s+.*)?$)?
                (.|\n)+?
            )
            ^}}})
        '''
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
            InlineRules.link,
            InlineRules.inline_macro, InlineRules.macro_tag,
            InlineRules.image,
            InlineRules.pre_inline
        ])

    # For pre escaping, in creole 1.0 done with ~:
    pre_escape = r' ^(?P<indent>\s*) ~ (?P<rest> \}\}\} \s*) $'



BLOCK_FLAGS = re.VERBOSE | re.UNICODE | re.MULTILINE
BLOCK_RULES = (
    BlockRules.macro_block,
    BlockRules.line, BlockRules.head, BlockRules.separator,
    BlockRules.pre_block, BlockRules.list,
    BlockRules.table, BlockRules.text,
)

INLINE_FLAGS = re.VERBOSE | re.UNICODE
INLINE_RULES = (
    InlineRules.link, InlineRules.url,
    InlineRules.inline_macro, InlineRules.macro_tag,
    InlineRules.pre_inline, InlineRules.image,

    InlineRules.strong, InlineRules.emphasis,
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
            print " -" * 39
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
        SpecialRules.pre_escape, re.MULTILINE | re.VERBOSE | re.UNICODE
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
        assert isinstance(raw, unicode)
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

    def _text_repl(self, groups):
#        print "_text_repl()", self.cur.kind, groups.get('break') != None
        if self.cur.kind in ('table', 'table_row', 'bullet_list',
                                                                'number_list'):
            self._upto_block()

        if self.cur.kind in ('document', 'section', 'blockquote'):
            self.cur = DocNode('paragraph', self.cur)

        self.parse_inline(groups.get('text', u""))

        if groups.get('break') and self.cur.kind in ('paragraph',
            'emphasis', 'strong', 'pre_inline'):
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

    #--------------------------------------------------------------------------

    def _add_macro(self, groups, macro_type, name_key, args_key, text_key=None):
        """
        generic mathod to handle the macro, used for all variants:
        inline, inline-tag, block
        """
        #self.debug_groups(groups)
        assert macro_type in ("macro_inline", "macro_block")

        if text_key:
            macro_text = groups.get(text_key, u"").strip()
        else:
            macro_text = None

        node = DocNode(macro_type, self.cur, macro_text)
        node.macro_name = groups[name_key]
        node.macro_args = groups.get(args_key, u"").strip()

        self.text = None

    def _macro_block_repl(self, groups):
        """
        block macro, e.g:
        <<macro args="foo">>
        some
        lines
        <</macro>>
        """
        self._upto_block()
        self.cur = self.root
        self._add_macro(
            groups,
            macro_type=u"macro_block",
            name_key=u"macro_block_start",
            args_key=u"macro_block_args",
            text_key=u"macro_block_text",
        )
    _macro_block_start_repl = _macro_block_repl
    _macro_block_args_repl = _macro_block_repl
    _macro_block_text_repl = _macro_block_repl

    def _macro_tag_repl(self, groups):
        """
        A single macro tag, e.g.: <<macro-a foo="bar">> or <<macro />>
        """
        self._add_macro(
            groups,
            macro_type=u"macro_inline",
            name_key=u"macro_tag_name",
            args_key=u"macro_tag_args",
            text_key=None,
        )
    _macro_tag_name_repl = _macro_tag_repl
    _macro_tag_args_repl = _macro_tag_repl


    def _macro_inline_repl(self, groups):
        """
        inline macro tag with data, e.g.: <<macro>>text<</macro>>
        """
        self._add_macro(
            groups,
            macro_type=u"macro_inline",
            name_key=u"macro_inline_start",
            args_key=u"macro_inline_args",
            text_key=u"macro_inline_text",
        )
    _macro_inline_start_repl = _macro_inline_repl
    _macro_inline_args_repl = _macro_inline_repl
    _macro_inline_text_repl = _macro_inline_repl

    #--------------------------------------------------------------------------

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
        """ List item """
        bullet = groups.get('item_head', u"")
        text = groups.get('item_text', u"")
        if bullet[-1] == '#':
            kind = 'number_list'
        else:
            kind = 'bullet_list'
        level = len(bullet) - 1
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
        self.cur.level = level + 1
        self.parse_inline(text)
        self.text = None
    _item_text_repl = _item_repl
    _item_head_repl = _item_repl

    def _list_repl(self, groups):
        """ complete list """
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

    def _pre_block_repl(self, groups):
        self._upto_block()
        kind = groups.get('pre_block_kind', None)
        text = groups.get('pre_block_text', u"")
        def remove_tilde(m):
            return m.group('indent') + m.group('rest')
        text = self.pre_escape_re.sub(remove_tilde, text)
        node = DocNode('pre_block', self.cur, text)
        node.sect = kind or ''
        self.text = None
    _pre_block_text_repl = _pre_block_repl
    _pre_block_head_repl = _pre_block_repl
    _pre_block_kind_repl = _pre_block_repl

    def _line_repl(self, groups):
        """ Transfer newline from the original markup into the html code """
        self._upto_block()
        DocNode('line', self.cur, u"")

    def _pre_inline_repl(self, groups):
        text = groups.get('pre_inline_text', u"")
        DocNode('pre_inline', self.cur, text)
        self.text = None
    _pre_inline_text_repl = _pre_inline_repl
    _pre_inline_head_repl = _pre_inline_repl

    #--------------------------------------------------------------------------

    def _inline_mark(self, groups, key):
        self.cur = DocNode(key, self.cur)

        self.text = None
        text = groups["%s_text" % key]
        self.parse_inline(text)

        self.cur = self._upto(self.cur, (key,)).parent
        self.text = None


    # TODO: How can we generalize that:
    def _emphasis_repl(self, groups):
        self._inline_mark(groups, key='emphasis')
    _emphasis_text_repl = _emphasis_repl

    def _strong_repl(self, groups):
        self._inline_mark(groups, key='strong')
    _strong_text_repl = _strong_repl

    def _monospace_repl(self, groups):
        self._inline_mark(groups, key='monospace')
    _monospace_text_repl = _monospace_repl

    def _superscript_repl(self, groups):
        self._inline_mark(groups, key='superscript')
    _superscript_text_repl = _superscript_repl

    def _subscript_repl(self, groups):
        self._inline_mark(groups, key='subscript')
    _subscript_text_repl = _subscript_repl

    def _underline_repl(self, groups):
        self._inline_mark(groups, key='underline')
    _underline_text_repl = _underline_repl

    def _small_repl(self, groups):
        self._inline_mark(groups, key='small')
    _small_text_repl = _small_repl

    def _delete_repl(self, groups):
        self._inline_mark(groups, key='delete')
    _delete_text_repl = _delete_repl

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

#        def debug(groups):
#            from pprint import pformat
#            data = dict([
#                group for group in groups.iteritems() if group[1] is not None
#            ])
#            print "%s\n" % pformat(data)

        groups = match.groupdict()
        for name, text in groups.iteritems():
            if text is not None:
                #if name != "char": debug(groups)
                replace_method = getattr(self, '_%s_repl' % name)
                replace_method(groups)
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
        print "_" * 80

        if start_node == None:
            start_node = self.root
            print "  document tree:"
        else:
            print "  tree from %s:" % start_node

        print "=" * 80
        def emit(node, ident=0):
            for child in node.children:
                print u"%s%s: %r" % (u" " * ident, child.kind, child.content)
                emit(child, ident + 4)
        emit(start_node)
        print "*" * 80

    def debug_groups(self, groups):
        print "_" * 80
        print "  debug groups:"
        for name, text in groups.iteritems():
            if text is not None:
                print "%15s: %r" % (name, text)
        print "-" * 80



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
            assert isinstance(content, unicode)
        self.content = content

        if self.parent is not None:
            self.parent.children.append(self)

    def __str__(self):
#        return "DocNode kind '%s', content: %r" % (self.kind, self.content)
        return "<DocNode %s: %r>" % (self.kind, self.content)
    def __repr__(self):
        return u"<DocNode %s: %r>" % (self.kind, self.content)

    def debug(self):
        print "_" * 80
        print "\tDocNode - debug:"
        print "str(): %s" % self
        print "attributes:"
        for i in dir(self):
            if i.startswith("_"):
                continue
            print "%20s: %r" % (i, getattr(self, i, "---"))


#------------------------------------------------------------------------------


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print "doc test done."

    print "-" * 80

    txt = u"""
Bold and italics should //be
able// to cross lines.

But, should //not be...

...able// to cross paragraphs.
"""

    print txt
    print "-" * 80

    p = Parser(txt)
    document = p.parse()
    p.debug()

    def display_match(match):
        groups = match.groupdict()
        for name, text in groups.iteritems():
            if name != "char" and text != None:
                print "%20s: %r" % (name, text)


    parser = Parser(u"")

    print "_" * 80
    print "merged block rules test:"
    re.sub(parser.block_re, display_match, txt)

    print "_" * 80
    print "merged inline rules test:"
    re.sub(parser.inline_re, display_match, txt)


    def test_single(rules, flags, txt):
        for rule in rules:
            rexp = re.compile(rule, flags)
            rexp.sub(display_match, txt)

    print "_" * 80
    print "single block rules match test:"
    test_single(BLOCK_RULES, BLOCK_FLAGS, txt)

    print "_" * 80
    print "single inline rules match test:"
    test_single(INLINE_RULES, INLINE_FLAGS, txt)


    print "---END---"
