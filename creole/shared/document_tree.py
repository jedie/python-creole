#!/usr/bin/env python
# coding: utf-8

"""
    python-creole
    ~~~~~~~~~~~~~


    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import warnings
import inspect

from creole.py3compat import TEXT_TYPE
from creole.shared.utils import dict2string


class DocNode:
    """
    A node in the document tree for html2creole and creole2html.
    
    The Document tree would be created in the parser and used in the emitter.
    """
    def __init__(self, kind='', parent=None, content=None, attrs=[], level=None):
        self.kind = kind

        self.children = []
        self.parent = parent
        if self.parent is not None:
            self.parent.children.append(self)

        self.attrs = dict(attrs)
        if content:
            assert isinstance(content, TEXT_TYPE), "Given content %r is not unicode, it's type: %s" % (
                content, type(content)
            )

        self.content = content
        self.level = level

    def get_attrs_as_string(self):
        """
        FIXME: Find a better was to do this.

        >>> node = DocNode(attrs={'foo':"bar", "no":123})
        >>> node.get_attrs_as_string()
        "foo='bar' no=123"

        >>> node = DocNode(attrs={"foo":'bar', "no":"ABC"})
        >>> node.get_attrs_as_string()
        "foo='bar' no='ABC'"
        """
        return dict2string(self.attrs)

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return "<DocNode %s: %r>" % (self.kind, self.content)
#        return "<DocNode %s (parent: %r): %r>" % (self.kind, self.parent, self.content)

    def debug(self):
        print("_" * 80)
        print("\tDocNode - debug:")
        print("str(): %s" % self)
        print("attributes:")
        for i in dir(self):
            if i.startswith("_") or i == "debug":
                continue
            print("%20s: %r" % (i, getattr(self, i, "---")))


class DebugList(list):
    def __init__(self, html2creole):
        self.html2creole = html2creole
        super(DebugList, self).__init__()

    def append(self, item):
#        for stack_frame in inspect.stack(): print(stack_frame)

        line, method = inspect.stack()[1][2:4]
        msg = "%-8s   append: %-35r (%-15s line:%s)" % (
            self.html2creole.getpos(), item,
            method, line
        )
        warnings.warn(msg)
        list.append(self, item)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
