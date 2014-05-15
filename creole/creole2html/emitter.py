# coding: utf-8


"""
    WikiCreole to HTML converter

    :copyleft: 2008-2014 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from __future__ import division, absolute_import, print_function, unicode_literals

from xml.sax.saxutils import escape
import sys
import traceback

from creole.creole2html.parser import CreoleParser
from creole.py3compat import TEXT_TYPE, repr2
from creole.shared.utils import string2dict



class TableOfContent(object):
    def __init__(self):
        self.max_depth = None
        self.headlines = []
        self._created = False
        self._current_level = 0

    def __call__(self, depth=None, **kwargs):
        """Called when if the macro <<toc>> is defined when it is emitted."""
        if self._created:
            return "&lt;&lt;toc&gt;&gt;"

        self._created = True
        if depth is not None:
            self.max_depth = depth

        return '<<toc>>'

    def add_headline(self, level, content):
        """Add the current header to the toc."""
        if self.max_depth is None or level <= self.max_depth:
            self.headlines.append(
                (level, content)
            )

    def flat_list2nest_list(self, flat_list):
        # this func code based on borrowed code from EyDu, Thanks!
        # http://www.python-forum.de/viewtopic.php?p=258121#p258121
        tree = []
        stack = [tree]

        for index, element in flat_list:
            stack_length = len(stack)

            if index > stack_length:
                for _ in range(stack_length, index):
                    l = []
                    stack[-1].append(l)
                    stack.append(l)
            elif index < stack_length:
                stack = stack[:index]

            stack[-1].append(element)

        return tree

    def nested_headlines2html(self, nested_headlines, level=0):
        """Convert a python nested list like the one representing the toc to an html equivalent."""
        indent = "\t"*level
        if isinstance(nested_headlines, TEXT_TYPE):
            return '%s<li><a href="#%s">%s</a></li>\n' % (indent, nested_headlines, nested_headlines)
        elif isinstance(nested_headlines, list):
            html = '%s<ul>\n' % indent
            for elt in nested_headlines:
                html += self.nested_headlines2html(elt, level + 1)
            html += '%s</ul>' % indent
            if level > 0:
                html += "\n"
            return html

    def emit(self, document):
        """Emit the toc where the <<toc>> macro was."""
        nested_headlines = self.flat_list2nest_list(self.headlines)
        html = self.nested_headlines2html(nested_headlines)

        # FIXME: We should not use <p> here, because it doesn't match
        #        if no newline was made before <<toc>>
        if "<p><<toc>></p>" in document:
            document = document.replace("<p><<toc>></p>", html, 1)
        else:
            document = document.replace("<<toc>>", html, 1)

        return document



class HtmlEmitter(object):
    """
    Generate HTML output for the document
    tree consisting of DocNodes.
    """
    def __init__(self, root, macros=None, verbose=None, stderr=None):
        self.root = root


        if callable(macros) == True:
            # was a DeprecationWarning in the past
            raise TypeError("Callable macros are not supported anymore!")

        if macros is None:
            self.macros = {}
        else:
            self.macros = macros

        if not "toc" in root.used_macros:
            # The document has no <<toc>>
            self.toc = None
        else:
            if isinstance(self.macros, dict):
                if "toc" in self.macros:
                    self.toc = self.macros["toc"]
                else:
                    self.toc = TableOfContent()
                    self.macros["toc"] = self.toc
            else:
                try:
                    self.toc = getattr(self.macros, "toc")
                except AttributeError:
                    self.toc = TableOfContent()
                    self.macros.toc = self.toc


        if verbose is None:
            self.verbose = 1
        else:
            self.verbose = verbose

        if stderr is None:
            self.stderr = sys.stderr
        else:
            self.stderr = stderr

    def get_text(self, node):
        """Try to emit whatever text is in the node."""
        try:
            return node.children[0].content or ''
        except:
            return node.content or ''

    def html_escape(self, text):
        return escape(text)

    def attr_escape(self, text):
        return self.html_escape(text).replace('"', '&quot')

    # *_emit methods for emitting nodes of the document:

    def document_emit(self, node):
        return self.emit_children(node)

    def text_emit(self, node):
        return self.html_escape(node.content)

    def separator_emit(self, node):
        return '<hr />\n\n'

    def paragraph_emit(self, node):
        return '<p>%s</p>\n' % self.emit_children(node)

    def _list_emit(self, node, list_type):
        if node.parent.kind in ("document",):
            # The first list item
            formatter = ''
        else:
            formatter = '\n'

        if list_type == "li":
            formatter += (
                '%(i)s<%(t)s>%(c)s</%(t)s>'
            )
        else:
            formatter += (
                '%(i)s<%(t)s>%(c)s\n'
                '%(i)s</%(t)s>'
            )
        return formatter % {
            "i": "\t" * node.level,
            "c": self.emit_children(node),
            "t": list_type,
        }

    def bullet_list_emit(self, node):
        return self._list_emit(node, list_type="ul")

    def number_list_emit(self, node):
        return self._list_emit(node, list_type="ol")

    def list_item_emit(self, node):
        return self._list_emit(node, list_type="li")

    def table_emit(self, node):
        return '<table>\n%s</table>\n' % self.emit_children(node)

    def table_row_emit(self, node):
        return '<tr>\n%s</tr>\n' % self.emit_children(node)

    def table_cell_emit(self, node):
        return '\t<td>%s</td>\n' % self.emit_children(node)

    def table_head_emit(self, node):
        return '\t<th>%s</th>\n' % self.emit_children(node)

    #--------------------------------------------------------------------------

    def _typeface(self, node, tag):
        return '<%(tag)s>%(data)s</%(tag)s>' % {
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
        header = '<h%d>%s</h%d>' % (
                node.level, self.html_escape(node.content), node.level
        )
        if self.toc is not None:
            self.toc.add_headline(node.level, node.content)
            # add link attribute for toc navigation
            header = '<a name="%s">%s</a>' % (
                self.html_escape(node.content), header
            )

        header += "\n"
        return header

    def preformatted_emit(self, node):
        return '<pre>%s</pre>' % self.html_escape(node.content)

    def link_emit(self, node):
        target = node.content
        if node.children:
            inside = self.emit_children(node)
        else:
            inside = self.html_escape(target)

        return '<a href="%s">%s</a>' % (
            self.attr_escape(target), inside)

    def image_emit(self, node):
        target = node.content
        text = self.attr_escape(self.get_text(node))

        return '<img src="%s" title="%s" alt="%s" />' % (
            self.attr_escape(target), text, text)

    def macro_emit(self, node):
        #print(node.debug())
        macro_name = node.macro_name
        text = node.content
        macro = None

        args = node.macro_args
        try:
            macro_kwargs = string2dict(args)
        except ValueError as e:
            exc_info = sys.exc_info()
            return self.error(
                "Wrong macro arguments: %s for macro '%s' (maybe wrong macro tag syntax?)" % (
                    repr2(args), macro_name
                ),
                exc_info
            )

        macro_kwargs["text"] = text

        exc_info = None
        if isinstance(self.macros, dict):
            try:
                macro = self.macros[macro_name]
            except KeyError as e:
                exc_info = sys.exc_info()
        else:
            try:
                macro = getattr(self.macros, macro_name)
            except AttributeError as e:
                exc_info = sys.exc_info()

        if macro == None:
            return self.error(
                "Macro '%s' doesn't exist" % macro_name,
                exc_info
            )

        try:
            result = macro(**macro_kwargs)
        except TypeError as err:
            msg = "Macro '%s' error: %s" % (macro_name, err)
            exc_info = sys.exc_info()
            if self.verbose > 1:
                if self.verbose > 2:
                    raise

                # Inject more information about the macro in traceback
                etype, evalue, etb = exc_info
                import inspect
                try:
                    filename = inspect.getfile(macro)
                except TypeError:
                    pass
                else:
                    try:
                        sourceline = inspect.getsourcelines(macro)[0][0].strip()
                    except IOError as err:
                        evalue = etype("%s (error getting sourceline: %s from %s)" % (evalue, err, filename))
                    else:
                        evalue = etype("%s (sourceline: %r from %s)" % (evalue, sourceline, filename))
                    exc_info = etype, evalue, etb

            return self.error(msg, exc_info)
        except Exception as err:
            return self.error(
                "Macro '%s' error: %s" % (macro_name, err),
                exc_info=sys.exc_info()
            )

        if not isinstance(result, TEXT_TYPE):
            msg = "Macro '%s' doesn't return a unicode string!" % macro_name
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
            return "<br />\n" + "\t" * node.parent.level
        elif node.parent.kind in ("table_head", "table_cell"):
            return "<br />\n\t\t"
        else:
            return "<br />\n"

    def line_emit(self, node):
        return "\n"

    def pre_block_emit(self, node):
        """ pre block, with newline at the end """
        return "<pre>%s</pre>\n" % self.html_escape(node.content)

    def pre_inline_emit(self, node):
        """ pre without newline at the end """
        return "<tt>%s</tt>" % self.html_escape(node.content)

    def default_emit(self, node):
        """Fallback function for emitting unknown nodes."""
        raise NotImplementedError("Node '%s' unknown" % node.kind)

    def emit_children(self, node):
        """Emit all the children of a node."""
        return ''.join([self.emit_node(child) for child in node.children])

    def emit_node(self, node):
        """Emit a single node."""
        #print("%s_emit: %r" % (node.kind, node.content))
        emit = getattr(self, '%s_emit' % node.kind, self.default_emit)
        return emit(node)

    def emit(self):
        """Emit the document represented by self.root DOM tree."""
        document = self.emit_node(self.root).strip()
        if self.toc is not None:
            return self.toc.emit(document)
        else:
            return document

    def error(self, text, exc_info=None):
        """
        Error Handling.
        """
        if self.verbose > 1 and exc_info:
            exc_type, exc_value, exc_traceback = exc_info
            exception = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            self.stderr.write(exception)

        if self.verbose > 0:
            return "[Error: %s]\n" % text
        else:
            # No error output
            return ""


if __name__ == "__main__":
    txt = """Local test
<<toc>>
= headline 1 level 1
== headline 2 level 2
== headline 3 level 2
==== headline 4 level 4
= headline 5 level 1
=== headline 6 level 3
"""

    print("-" * 80)
#    from creole_alt.creole import CreoleParser
    p = CreoleParser(txt)
    document = p.parse()
    p.debug()

    html = HtmlEmitter(document, verbose=999).emit()
    print(html)
    print("-" * 79)
    print(html.replace(" ", ".").replace("\n", "\\n\n"))
