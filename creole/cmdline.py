#!/usr/bin/env python
# coding: utf-8

"""
    python-creole commandline interface
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2013 by the python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals
import argparse
import codecs

from creole import creole2html, html2creole, html2rest, html2textile
from creole import VERSION_STRING


class CreoleCLI(object):
    def __init__(self, convert_func):
        self.convert_func = convert_func
        self.parser = argparse.ArgumentParser(
            description=(
                "python-creole is an open-source (GPL) markup converter"
                " in pure Python for:"
                " creole2html, html2creole, html2ReSt, html2textile"
            ),
            version=VERSION_STRING,
        )

        self.parser.add_argument("sourcefile", help="source file to convert")
        self.parser.add_argument("destination", help="Output filename")
        self.parser.add_argument("--encoding",
            default="utf-8",
            help="Codec for read/write file (default encoding: utf-8)"
        )
        
        args = self.parser.parse_args()

        sourcefile = args.sourcefile
        destination = args.destination
        encoding = args.encoding

        self.convert(sourcefile, destination, encoding)

    def convert(self, sourcefile, destination, encoding):
        print("Convert %r to %r with %s (codec: %s)" % (
            sourcefile, destination, self.convert_func.__name__, encoding
        ))
        
        with codecs.open(sourcefile, "r", encoding=encoding) as infile:
            with codecs.open(destination, "w", encoding=encoding) as outfile:
                content = infile.read()
                converted = self.convert_func(content)
                outfile.write(converted)
        print("done. %r created." % destination)


def cli_creole2html():
    cli = CreoleCLI(creole2html)
#     cli.convert()

def cli_html2creole():
    cli = CreoleCLI(html2creole)
#     cli.convert()
    
def cli_html2rest():
    cli = CreoleCLI(html2rest)
#     cli.convert()
    
def cli_html2textile():
    cli = CreoleCLI(html2textile)
#     cli.convert()


if __name__ == "__main__":
    import sys
    sys.argv += ["../README.creole", "../test.html"]
    print(sys.argv)
    cli_creole2html()
