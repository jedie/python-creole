#!/usr/bin/env python3


"""
    simple demo
    ~~~~~~~~~~~
"""


from creole import creole2html, html2creole, html2rest, html2textile


source_creole = """\
== simple demo

You can convert from:

* **creole2html**, **html2creole**, **html2rest**, //html2textile//

=== a table:

|=headline 1 |= headline 2 |
| 1.1. cell  | 1.2. cell   |
| 2.1. cell  | 2.2. cell   |

----

More info on our [[http://code.google.com/p/python-creole/|Homepage]]."""


if __name__ == "__main__":
    print("_" * 79 + "\n*** Convert creole into html: ***\n\n")
    html = creole2html(source_creole)
    print(html)

    print("\n\n" + "_" * 79 + "\n*** Convert html back into creole: ***\n\n")
    creole = html2creole(html)
    print(creole)

    print("\n\n" + "_" * 79 + "\n*** Convert html into ReStructuredText: ***\n\n")
    rest = html2rest(html)
    print(rest)

    print("\n\n" + "_" * 79 + "\n*** Convert html into textile: ***\n\n")
    textile = html2textile(html)
    print(textile)
