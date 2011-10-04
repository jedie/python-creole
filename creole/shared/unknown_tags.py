#!/usr/bin/env python
# coding: utf-8


"""
    python-creole
    ~~~~~~~~~~~~~


    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

from xml.sax.saxutils import escape


def _mask_content(emitter, node, mask_tag):
    attrs = node.get_attrs_as_string()
    if attrs:
        attrs = " " + attrs

    tag_data = {
        "tag": node.kind,
        "attrs": attrs,
        "mask_tag": mask_tag,
    }

    content = emitter.emit_children(node)
    if not content:
        # single tag
        return "<<%(mask_tag)s>><%(tag)s%(attrs)s /><</%(mask_tag)s>>" % tag_data

    start_tag = "<<%(mask_tag)s>><%(tag)s%(attrs)s><</%(mask_tag)s>>" % tag_data
    end_tag = "<<%(mask_tag)s>></%(tag)s><</%(mask_tag)s>>" % tag_data

    return start_tag + content + end_tag



def raise_unknown_node(emitter, node):
    """
    unknown_emit callable for Html2CreoleEmitter
    
    Raise NotImplementedError on unknown tags.
    """
    content = emitter.emit_children(node)
    raise NotImplementedError(
        "Node from type '%s' is not implemented! (child content: %r)" % (
            node.kind, content
        )
    )


def use_html_macro(emitter, node):
    """
    unknown_emit callable for Html2CreoleEmitter
    
    Use the <<html>> macro to mask unknown tags.
    """
    return _mask_content(emitter, node, mask_tag="html")


def preformat_unknown_nodes(emitter, node):
    """
    Put unknown tags in a <pre> area.
    
    Usefull for html2textile.emitter.TextileEmitter()
    """
    return _mask_content(emitter, node, mask_tag="pre")


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
        return escape("<%(tag)s%(attrs)s />" % tag_data)

    start_tag = escape("<%(tag)s%(attrs)s>" % tag_data)
    end_tag = escape("</%(tag)s>" % tag_data)

    return start_tag + content + end_tag


def transparent_unknown_nodes(emitter, node):
    """
    unknown_emit callable for Html2CreoleEmitter 
    
    Remove all unknown html tags and show only
    their child nodes' content.
    """
    return emitter._emit_content(node)
