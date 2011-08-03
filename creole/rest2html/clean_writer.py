#!/usr/bin/env python
# coding: utf-8

"""
    Some code stolen from:
    http://www.arnebrodowski.de/blog/write-your-own-restructuredtext-writer.html
"""


import warnings


try:
    from docutils.core import publish_parts
except ImportError:
    REST_INSTALLED = False
    warnings.warn(
        "Markup error: 'Python Documentation Utilities' isn't installed. Can't test reStructuredText."
        " Download: http://pypi.python.org/pypi/docutils"
    )
else:
    REST_INSTALLED = True


from docutils.writers import html4css1


DEBUG = False
#DEBUG = True

IGNORE_ATTR = (
    "class",
)


class CleanHTMLWriter(html4css1.Writer):
    """
    This docutils writer will use the CleanHTMLTranslator class below.
    """
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = CleanHTMLTranslator

class CleanHTMLTranslator(html4css1.HTMLTranslator):
    """
    This is a translator class for the docutils system.
    It will produce a minimal set of html output.
    (No extry divs, classes oder ids.)
    """
    def _do_nothing(self, node, *args, **kwargs):
        pass

    def starttag(self, node, tagname, suffix='\n', empty=0, **attributes):
        if DEBUG:
            print "ids: %r" % getattr(node, "ids", "-")
        node.ids = []
        if DEBUG:
            print "attributes: %r" % attributes
        for attr in IGNORE_ATTR:
            for attr2 in (attr, attr.lower(), attr.upper()):
                if attr2 in attributes:
                    del(attributes[attr2])

        return html4css1.HTMLTranslator.starttag(self, node, tagname, suffix, empty, **attributes)

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    set_class_on_child = _do_nothing
    set_first_last = _do_nothing

    def visit_list_item(self, node):
        # FIXME: How to remove class="first" in: <li><p class="first">item 1</p>
        #        in a generally way?
        self.body.append(self.starttag(node, 'li', ''))

    # remove <blockquote> (e.g. in nested lists)
    visit_block_quote = _do_nothing
    depart_block_quote = _do_nothing

    #__________________________________________________________________________
    # Clean table:

    visit_thead = _do_nothing
    depart_thead = _do_nothing
    visit_tbody = _do_nothing
    depart_tbody = _do_nothing

    def visit_table(self, node):
        self.body.append(self.starttag(node, 'table'))

    def visit_tgroup(self, node):
        node.stubs = []


def rest2html(content):
    """
    Convert reStructuredText markup to clean html code: No extra div, class or ids.
    
    >>> rest2html(u"- bullet list")
    u'<ul>\\n<li>bullet list</li>\\n</ul>\\n'
    """
    parts = publish_parts(
        source=content,
#        writer_name="html4css1",
        writer=CleanHTMLWriter(),
        settings_overrides={
            "input_encoding": "unicode",
            "doctitle_xform": False,
        },
    )
    return parts["fragment"]


if __name__ == '__main__':
    import doctest
    print doctest.testmod()

#    print rest2html(u"""
#+------------+------------+
#| Headline 1 | Headline 2 |
#+============+============+
#| cell one   | cell two   |
#+------------+------------+
#    """)

    print rest2html(u"""
- item 1

    - subitem 1.1

    - subitem 1.2

- item 2

    - subitem 2.1
    """)
