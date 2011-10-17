#!/usr/bin/env python
# coding: utf-8

"""
    collects all existing unittests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

from creole.tests.test_creole2html import TestCreole2html, TestCreole2htmlMarkup, TestStr2Dict, TestDict2String
from creole.tests.test_cross_compare_all import CrossCompareTests
from creole.tests.test_cross_compare_creole import CrossCompareCreoleTests
from creole.tests.test_cross_compare_rest import CrossCompareReStTests
from creole.tests.test_cross_compare_textile import CrossCompareTextileTests
from creole.tests.test_html2creole import TestHtml2Creole, TestHtml2CreoleMarkup
from creole.tests.test_rest2html import ReSt2HtmlTests
from creole.tests.test_setup_utils import SetupUtilsTests
from creole.tests.test_utils import UtilsTests
from creole.tests.utils.utils import MarkupTest
