# coding: utf-8

"""
    utils for distutils setup
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Get README.creole as ReStructuredText on-the-fly for setup.long_description
    
    More information:
        https://code.google.com/p/python-creole/wiki/UseInSetup
    
    usage in setup.py e.g.:
    ---------------------------------------------------------------------------
    #!/usr/bin/env python
    # coding: utf-8
    
    import os
    import sys
    from setuptools import setup, find_packages
    
    try:
        from creole.setup_utils import GetLongDescription
    except ImportError:
        if "register" in sys.argv or "sdist" in sys.argv or "--long-description" in sys.argv:
            etype, evalue, etb = sys.exc_info()
            evalue = etype("%s - Please install python-creole >= v0.8 -  e.g.: pip install python-creole" % evalue)
            raise etype, evalue, etb
        GetLongDescription = None
    
    PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
    
    setup(
        ...
        long_description=GetLongDescription(PACKAGE_ROOT),
        ...
    )
    ---------------------------------------------------------------------------
    
    :copyleft: 2011 by the python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import codecs
import os
import sys

from creole import creole2html, html2rest


class GetLongDescription(object):
    """
    Read and convert README.creole lazy to ReStructuredText.
    """
    RAISE_ERRORS_ARGS = ("register", "sdist", "--long-description")

    def __init__(self, package_root, filename="README.creole", raise_errors=None):
        self.package_root = package_root
        self.filename = filename
        self.raise_errors = raise_errors

        self.long_description_origin = ""
        self.long_description_html = None
        self.long_description_rest_unicode = None
        self.long_description_rest = None

    def should_raise_errors(self):
        """
        Raise only errors, if one of self.RAISE_ERRORS_ARGS is in sys.argv
        or if no argument presents.
        """
        if len(sys.argv) == 1:
            return True

        for arg in self.RAISE_ERRORS_ARGS:
            if arg in sys.argv:
                return True
        return False

    def read_long_description(self):
        """ read README file and convert it to ReStructuredText. """
        if self.raise_errors is None:
            self.raise_errors = self.should_raise_errors()

        if self.raise_errors:
            # raise a error if a unknown node found
            from creole.shared.unknown_tags import raise_unknown_node as unknown_emit
        else:
            # ignore unknown nodes
            from creole.shared.unknown_tags import transparent_unknown_nodes as unknown_emit

        filepath = os.path.join(self.package_root, self.filename)
        try:
            # Read creole README
            f = codecs.open(filepath, "r", encoding="utf-8")
            self.long_description_origin = f.read().strip()
            f.close()

            # convert creole into html
            self.long_description_html = creole2html(self.long_description_origin)

            # convert html to ReSt
            self.long_description_rest_unicode = html2rest(
                self.long_description_html,
                emitter_kwargs={"unknown_emit":unknown_emit}
            )
            self.long_description_rest = self.long_description_rest_unicode.encode("utf-8")
        except Exception, err:
            if self.raise_errors:
                raise
            # Don't raise the error e.g. in ./setup install process
            self.long_description_rest = "[Error: %s]\n%s" % (
                err, self.long_description_origin
            )
        else:
            if self.raise_errors:
                # Test created ReSt code
                from creole.rest2html.clean_writer import rest2html
                rest2html(self.long_description_rest_unicode)

    def __str__(self):
        if self.long_description_rest is None:
            self.read_long_description()
        return self.long_description_rest

    def __unicode__(self):
        if self.long_description_rest_unicode is None:
            self.read_long_description()
        return self.long_description_rest_unicode



if __name__ == "__main__":
    package_root = os.path.abspath("../")
    long_description = GetLongDescription(package_root)
    print long_description
