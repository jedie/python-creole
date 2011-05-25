#!/usr/bin/env python
# coding: utf-8


"""
    python-creole
    ~~~~~~~~~~~~~


    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from xml.sax.saxutils import escape


def raise_unknown_node(emitter, node):
    """
    unknown_emit callable for Html2CreoleEmitter
    
    Raise NotImplementedError on unknown tags.
    """
    raise NotImplementedError(
        "Node from type '%s' is not implemented!" % node.kind
    )


def use_html_macro(emitter, node):
    """
    unknown_emit callable for Html2CreoleEmitter
    
    Use the <<html>> macro to mask unknown tags.
    """
    attrs = node.get_attrs_as_string()
    if attrs:
        attrs = " " + attrs

    tag_data = {
        "tag": node.kind,
        "attrs": attrs,
    }

    content = emitter.emit_children(node)
    if not content:
        # single tag
        return u"<<html>><%(tag)s%(attrs)s /><</html>>" % tag_data

    start_tag = u"<<html>><%(tag)s%(attrs)s><</html>>" % tag_data
    end_tag = u"<<html>></%(tag)s><</html>>" % tag_data

    return start_tag + content + end_tag


def escape_unknown_nodes(emitter, node):
    """
    unknown_emit callable for Html2CreoleEmitter
    
    All unknown tags should be escaped.
    """
    attrs = node.get_attrs_as_string()
    if attrs:
        attrs = " " + attrs

    tag_data = {
        "tag": node.kind,
        "attrs": attrs,
    }

    content = emitter.emit_children(node)
    if not content:
        # single tag
        return escape(u"<%(tag)s%(attrs)s />" % tag_data)

    start_tag = escape(u"<%(tag)s%(attrs)s>" % tag_data)
    end_tag = escape(u"</%(tag)s>" % tag_data)

    return start_tag + content + end_tag


def transparent_unknown_nodes(emitter, node):
    """
    unknown_emit callable for Html2CreoleEmitter 
    
    Remove all unknown html tags and show only
    their child nodes' content.
    """
    return emitter._emit_content(node)
