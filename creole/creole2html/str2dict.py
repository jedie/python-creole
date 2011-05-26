# coding: utf-8


"""
    Creole Rules for parser
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Helper take from PyLucid CMS project

    :copyleft: 2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import shlex


# For str2dict()
KEYWORD_MAP = {
    "True": True,
    "False": False,
    "None": None,
}

def str2dict(raw_content, encoding="utf-8"):
    """
    convert a string into a dictionary. e.g.:

    >>> str2dict('key1="value1" key2="value2"')
    {'key2': 'value2', 'key1': 'value1'}

    >>> str2dict(u'A="B" C=1 D=1.1 E=True F=False G=None')
    {'A': 'B', 'C': 1, 'E': True, 'D': '1.1', 'G': None, 'F': False}
    
    >>> str2dict('''key1="'1'" key2='"2"' key3="""'3'""" ''')
    {'key3': 3, 'key2': 2, 'key1': 1}

    >>> str2dict(u'unicode=True')
    {'unicode': True}
    """
    if isinstance(raw_content, unicode):
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


if __name__ == "__main__":
    import doctest
    print doctest.testmod()
