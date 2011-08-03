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

    #__________________________________________________________________________
    # Clean table:

    def do_nothing(self, node):
        pass
    visit_thead = do_nothing
    depart_thead = do_nothing
    visit_tbody = do_nothing
    depart_tbody = do_nothing

    def visit_table(self, node):
        self.body.append(self.starttag(node, 'table'))

    def visit_tgroup(self, node):
        node.stubs = []

def rest2html(content):
    """
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

    print rest2html(u"""
+------------+------------+
| Headline 1 | Headline 2 |
+============+============+
| cell one   | cell two   |
+------------+------------+
    """)
