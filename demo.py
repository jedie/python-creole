#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    simple demo
    ~~~~~~~~~~~
"""

from creole import creole2html, html2creole

source = """\
== simple demo
You can convert from:

* from //creole// to **html**
* from **html** back to //creole//

=== e.g. a table:
|=headline 1 |= headline 2 |
| 1.1. cell  | 1.2. cell   |
| 2.1. cell  | 2.2. cell   |
----

More info on our [[http://code.google.com/p/python-creole/|Homepage]]."""

print "*"*79
print " Source creole markup text:"
print "-"*79
print source

print "*"*79
print " Convert it into html:"
print "-"*79
html = creole2html(source)
print html

print "*"*79
print " Convert the html code back into creole:"
print "-"*79
creole = html2creole(html)
print creole
