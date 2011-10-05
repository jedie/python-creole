# coding: utf-8


"""
    python creole utilities
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import shlex

from creole.py3compat import TEXT_TYPE, PY3, repr2


# For string2dict()
KEYWORD_MAP = {
    "True": True,
    "False": False,
    "None": None,
}

def string2dict(raw_content, encoding="utf-8"):
    """
    convert a string into a dictionary. e.g.:

    >>> string2dict('key1="value1" key2="value2"')
    {'key2': 'value2', 'key1': 'value1'}
    
    See test_creole2html.TestString2Dict()
    """
    if not PY3 and isinstance(raw_content, TEXT_TYPE):
        # shlex.split doesn't work with unicode?!?
        raw_content = raw_content.encode(encoding)

    parts = shlex.split(raw_content)

    result = {}
    for part in parts:
        key, value = part.split("=", 1)

        if value in KEYWORD_MAP:
            # True False or None
            value = KEYWORD_MAP[value]
        else:
            # A number?
            try:
                value = int(value.strip("'\""))
            except ValueError:
                pass

        result[key] = value

    return result


def dict2string(d):
    """
    FIXME: Find a better was to do this.

    >>> dict2string({'foo':"bar", "no":123})
    "foo='bar' no=123"

    >>> dict2string({"foo":'bar', "no":"ABC"})
    "foo='bar' no='ABC'"
    
    See test_creole2html.TestDict2String()
    """
    attr_list = []
    for key, value in sorted(d.items()):
        value_string = repr2(value)
        attr_list.append("%s=%s" % (key, value_string))
    return " ".join(attr_list)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
