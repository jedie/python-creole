===================
about python-creole
===================

python-creole is a OpenSource (GPL) Python lib for converting markups.
python-creole is pure python. No external libs needed.

Compatible Python Versions (see `tox.ini <https://github.com/jedie/python-creole/blob/master/tox.ini>`_ or `.travis.yml <https://github.com/jedie/python-creole/blob/master/.travis.yml>`_):

* 3.9, 3.8, 3.7, 3.6

* PyPy3

Existing converters:

* creole -> html

* html -> creole markup

* reSt -> html (for clean html code)

* html -> reStructuredText markup (only a subset of reSt supported)

* html -> textile markup (not completed yet)

The creole2html part based on the creole markup parser and emitter from the MoinMoin project by Radomir Dopieralski and Thomas Waldmann.

+-----------------------------------+
| |Build Status on github|          |
+-----------------------------------+
| |Build Status on travis-ci.org|   |
+-----------------------------------+
| |Coverage Status on coveralls.io| |
+-----------------------------------+
| |Status on landscape.io|          |
+-----------------------------------+
| |PyPi version|                    |
+-----------------------------------+

.. |Build Status on github| image:: https://github.com/jedie/python-creole/workflows/test/badge.svg?branch=master
.. |Build Status on travis-ci.org| image:: https://travis-ci.org/jedie/python-creole.svg
.. _travis-ci.org/jedie/python-creole: https://travis-ci.org/jedie/python-creole/
.. |Coverage Status on coveralls.io| image:: https://coveralls.io/repos/jedie/python-creole/badge.svg
.. _coveralls.io/r/jedie/python-creole: https://coveralls.io/r/jedie/python-creole
.. |Status on landscape.io| image:: https://landscape.io/github/jedie/python-creole/master/landscape.svg
.. _landscape.io/github/jedie/python-creole/master: https://landscape.io/github/jedie/python-creole/master
.. |PyPi version| image:: https://badge.fury.io/py/python-creole.svg
.. _pypi.org/project/python-creole/: https://pypi.org/project/python-creole/

=======
install
=======

Python packages available on: `http://pypi.python.org/pypi/python-creole/ <http://pypi.python.org/pypi/python-creole/>`_

::

    ~$ pip install python-creole

To setup a virtualenv via Poetry, see ``unittests`` section below.

------------
dependencies
------------

For the most parts (``creole2html`` and ``html2creole``) no external libraries are needed.

For all functionality (and running the unittests) these modules are needed:

* `docutils <http://pypi.python.org/pypi/docutils/>`_ (for the ReStructuredText stuff)

* `textile <http://pypi.python.org/pypi/textile/>`_ (for html2textile tests)

=======
example
=======

-----------
creole2html
-----------

Convert creole markup to html code:

::

    >>> from creole import creole2html
    >>> creole2html("This is **creole //markup//**")
    u'<p>This is <strong>creole <i>markup</i></strong></p>\n'

-----------
html2creole
-----------

Convert html code back into creole markup:

::

    >>> from creole import html2creole
    >>> html2creole(u'<p>This is <strong>creole <i>markup</i></strong></p>\n')
    u'This is **creole //markup//**'

---------
rest2html
---------

Convert ReStructuredText into clean html code (needs `docutils`_):

::

    >>> from creole.rest2html.clean_writer import rest2html
    >>> rest2html(u"A ReSt link to `PyLucid CMS <http://www.pylucid.org>`_ :)")
    u'<p>A ReSt link to <a href="http://www.pylucid.org">PyLucid CMS</a> :)</p>\\n'

(more information: `rest2html wiki page <https://github.com/jedie/python-creole/wiki/rest2html>`_)

---------
html2rest
---------

Convert html code into ReStructuredText markup:

::

    >>> from creole import html2rest
    >>> html2rest(u'<p>This is <strong>ReStructuredText</strong> <em>markup</em>!</p>')
    u'This is **ReStructuredText** *markup*!'

------------
html2textile
------------

Convert html code into textile markup

::

    >>> from creole import html2textile
    >>> html2textile(u'<p>This is <strong>textile <i>markup</i></strong>!</p>')
    u'This is *textile __markup__*!'

See also: `http://github.com/jedie/python-creole/blob/master/demo.py <http://github.com/jedie/python-creole/blob/master/demo.py>`_

=====================
Image size additional
=====================

You can pass image width/height in image tags, e.g.:

::

    >>> from creole import creole2html
    >>> creole_markup="""{{foobar.jpg|image title|90x160}}"""
    >>> creole2html(creole_markup)
    '<p><img src="foobar.jpg" title="image title" alt="image title" width="90" height="160" /></p>'

The third part (``90x160``) is not in creole standard, you can force a *strict* mode, e.g.:

::

    >>> creole2html(creole_markup, strict=True)
    '<p><img src="foobar.jpg" title="image title|90x160" alt="image title|90x160" /></p>'

================================
Source code highlighting support
================================

You can find a example macro which highlight source code thanks to the pygments
library. It is located here: `/creole/shared/example_macros.py <https://github.com/jedie/python-creole/blob/master/creole/shared/example_macros.py>`_.
Here is how to use it:

::

    >>> from creole import creole2html
    >>> from creole.shared.example_macros import code
    >>> creole_markup="""<<code ext=".py">>#some code\nprint('coucou')\n<</code>>"""
    >>> creole2html(creole_markup, macros={'code': code})

=====================
commandline interface
=====================

If you have python-creole installed, you will get these simple CLI scripts:

* creole2html

* html2creole

* html2rest

* html2textile

Here the ``--help`` output from ``html2creole``:

::

    $ html2creole --help
    usage: html2creole [-h] [-v] [--encoding ENCODING] sourcefile destination
    
    python-creole is an open-source (GPL) markup converter in pure Python for:
    creole2html, html2creole, html2ReSt, html2textile
    
    positional arguments:
      sourcefile           source file to convert
      destination          Output filename
    
    optional arguments:
      -h, --help           show this help message and exit
      -v, --version        show program's version number and exit
      --encoding ENCODING  Codec for read/write file (default encoding: utf-8)

Example to convert a html file into a creole file:

::

    $ html2creole foobar.html foobar.creole

=============
documentation
=============

We store documentation/examples into the project wiki:

* `https://github.com/jedie/python-creole/wiki <https://github.com/jedie/python-creole/wiki>`_

How to handle unknown html tags in html2creole:

* `https://github.com/jedie/python-creole/wiki/Unknown-Html-Tags <https://github.com/jedie/python-creole/wiki/Unknown-Html-Tags>`_

Contributers should take a look at this page:

* `https://github.com/jedie/python-creole/wiki/Developer-Info <https://github.com/jedie/python-creole/wiki/Developer-Info>`_

Creole Markup Cheat Sheet can be found here: `http://www.wikicreole.org/wiki/CheatSheet <http://www.wikicreole.org/wiki/CheatSheet>`_

|Creole Markup Cheat Sheet|

.. |Creole Markup Cheat Sheet| image:: http://www.wikicreole.org/imageServlet?page=CheatSheet%2Fcreole_cheat_sheet.png&width=340

---------
unittests
---------

::

    # clone repository (or use your fork):
    ~$ git clone https://github.com/jedie/python-creole.git
    ~$ cd python-creole
    
    # install or update poetry:
    ~/python-creole$ make install-poetry
    
    # install python-creole via poetry:
    ~/python-creole$ make install
    
    # Run pytest:
    ~/python-creole$ make pytest
    
    # Run pytest via tox with all environments:
    ~/python-creole$ make tox
    
    # Run pytest via tox with one Python version:
    ~/python-creole$ make tox-py38
    ~/python-creole$ make tox-py37
    ~/python-creole$ make tox-py36

------------
make targets
------------

To see all make targets, just call ``make``:

::

    ~/python-creole$ make
    help                 List all commands
    install-poetry       install or update poetry
    install              install python-creole via poetry
    lint                 Run code formatters and linter
    fix-code-style       Fix code formatting
    tox-listenvs         List all tox test environments
    tox                  Run pytest via tox with all environments
    tox-py36             Run pytest via tox with *python v3.6*
    tox-py37             Run pytest via tox with *python v3.7*
    tox-py38             Run pytest via tox with *python v3.8*
    tox-py39             Run pytest via tox with *python v3.9*
    pytest               Run pytest
    update-rst-readme    update README.rst from README.creole
    publish              Release new version to PyPi

--------------------
Use creole in README
--------------------

With python-creole you can convert a README on-the-fly from creole into ReStructuredText in setup.py
How to do this, read: `https://github.com/jedie/python-creole/wiki/Use-In-Setup <https://github.com/jedie/python-creole/wiki/Use-In-Setup>`_

Note: In this case you must install **docutils**! See above.

=======
history
=======

* *dev* - `compare v1.4.9...master <https://github.com/jedie/python-creole/compare/v1.4.9...master>`_ 

    * TBC

* v1.4.9 - 2020-11-4 - `compare v1.4.8...v1.4.9 <https://github.com/jedie/python-creole/compare/v1.4.8...v1.4.9>`_ 

    * Add missing classifier for Python 3.9 (`Contributed by jugmac00 <https://github.com/jedie/python-creole/pull/55>`_)

    * Update readme test

* v1.4.8 - 2020-10-17 - `compare v1.4.7...v1.4.8 <https://github.com/jedie/python-creole/compare/v1.4.7...v1.4.8>`_ 

    * Validate generated ``README.rst`` with `readme-renderer <https://pypi.org/project/readme-renderer/>`_

* v1.4.7 - 2020-10-17 - `compare v1.4.6...v1.4.7 <https://github.com/jedie/python-creole/compare/v1.4.6...v1.4.7>`_ 

    * ``update_rst_readme()`` will touch ``README.rst`` if there are not change (timestamp will not changed in file)

    * Run tests with Python 3.9, too.

    * Some meta updates to project setup

* v1.4.6 - 2020-02-13 - `compare v1.4.5...v1.4.6 <https://github.com/jedie/python-creole/compare/v1.4.5...v1.4.6>`_ 

    * less restricted dependency specification

* v1.4.5 - 2020-02-13 - `compare v1.4.4...v1.4.5 <https://github.com/jedie/python-creole/compare/v1.4.4...v1.4.5>`_ 

    * new: ``creole.setup_utils.assert_rst_readme`` for project setup tests

    * use `https://github.com/ymyzk/tox-gh-actions <https://github.com/ymyzk/tox-gh-actions>`_ on gitlab CI

* v1.4.4 - 2020-02-07 - `compare v1.4.3...v1.4.4 <https://github.com/jedie/python-creole/compare/v1.4.3...v1.4.4>`_ 

    * Fix #44: Move ``poetry-publish`` to ``dev-dependencies`` and lower ``docutils`` requirement to |^0.15|

    * some code style updated

    * Always update README.rst before publish

* v1.4.3 - 2020-02-01 - `compare v1.4.2...v1.4.3 <https://github.com/jedie/python-creole/compare/v1.4.2...v1.4.3>`_ 

    * Use new `poetry-publish <https://pypi.org/project/poetry-publish/>`_ for ``make publish``

* v1.4.2 - 2020-02-01 - `compare v1.4.1...v1.4.2 <https://github.com/jedie/python-creole/compare/v1.4.1...v1.4.2>`_ 

    * Update CI configs on github and travis

    * Update ``Makefile``: add ``make publish`` and ``make update-rst-readme``

    * Add generated ``README.rst`` in repository to fix install problems about missing readme

* v1.4.1 - 2020-01-19 - `compare v1.4.0...v1.4.1 <https://github.com/jedie/python-creole/compare/v1.4.0...v1.4.1>`_ 

    * Remove Python v2 support code

    * `Fix "Undefined substitution referenced" error <https://github.com/jedie/python-creole/issues/26>`_ contributed by dforsi

    * `Fix regression in tests for setup_utils <https://github.com/jedie/python-creole/pull/37>`_ contributed by jugmac00

    * Fix code style with: autopep8

    * sort imports with isort

    * change old ``%-formatted`` and ``.format(...)`` strings into Python 3.6+'s ``f-strings`` with flynt

    * Activate linting in CI pipeline

* v1.4.0 - 2020-01-19 - `compare v1.3.2...v1.4.0 <https://github.com/jedie/python-creole/compare/v1.3.2...v1.4.0>`_ 

    * modernize project:

        * use poetry

        * Add a ``Makefile``

        * use pytest and tox

        * remove Python v2 support

        * Test with Python v3.6, v3.7 and v3.8

* v1.3.2 - 2018-02-27 - `compare v1.3.1...v1.3.2 <https://github.com/jedie/python-creole/compare/v1.3.1...v1.3.2>`_ 

    * Adding optional img size to creole2html and html2creole contributed by `John Dupuy <https://github.com/JohnAD>`_

    * run tests also with python 3.5 and 3.6

* v1.3.1 - 2015-08-15 - `compare v1.3.0...v1.3.1 <https://github.com/jedie/python-creole/compare/v1.3.0...v1.3.1>`_ 

    * Bugfix for "Failed building wheel for python-creole"

* v1.3.0 - 2015-06-02 - `compare v1.2.2...v1.3.0 <https://github.com/jedie/python-creole/compare/v1.2.2...v1.3.0>`_ 

    * Refactory internal file structure

    * run unittests and doctests with nose

    * Refactor CLI tests

    * skip official support for Python 2.6

    * small code cleanups and fixes.

    * use **json.dumps()** instead of **repr()** in some cases

* v1.2.2 - 2015-04-05 - `compare v1.2.1...v1.2.2 <https://github.com/jedie/python-creole/compare/v1.2.1...v1.2.2>`_ 

    * Bugfix textile unittests if url scheme is unknown

    * migrate google-code Wiki to github and remove google-code links

* v1.2.1 - 2014-09-14 - `compare v1.2.0...v1.2.1 <https://github.com/jedie/python-creole/compare/v1.2.0...v1.2.1>`_ 

    * Use origin PyPi code to check generated reStructuredText in setup.py

    * Update unitest for textile v2.1.8

* v1.2.0 - 2014-05-15 - `compare v1.1.1...v1.2.0 <https://github.com/jedie/python-creole/compare/v1.1.1...v1.2.0>`_ 

    * NEW: Add ``<<code>>`` example macro (Source code highlighting with pygments) - implemented by Julien Enselme

    * NEW: Add ``<<toc>>`` macro to create a table of contents list

    * Bugfix for: AttributeError: 'CreoleParser' object has no attribute '_escaped_char_repl'

    * Bugfix for: AttributeError: 'CreoleParser' object has no attribute '_escaped_url_repl'

    * API Change: Callable macros will raise a TypeError instead of create a DeprecationWarning (Was removed in v0.5)

* v1.1.1 - 2013-11-08

    * Bugfix: Setup script exited with error: can't copy 'README.creole': doesn't exist or not a regular file

* v1.1.0 - 2013-10-28

    * NEW: Simple commandline interface added.

* v1.0.7 - 2013-08-07

    * Bugfix in 'clean reStructuredText html writer' if docutils => v0.11 used.

    * Bugfix for PyPy 2.1 usage

* v1.0.6 - 2012-10-15

    * Security fix in rest2html: Disable "file_insertion_enabled" and "raw_enabled" as default.

* v1.0.5 - 2012-09-03

    * made automatic protocol links more strict: Only whitespace before and at the end are allowed.

    * Bugfix: Don't allow ``ftp:/broken`` (Only one slash) to be a link.

* v1.0.4 - 2012-06-11

    * html2rest: Handle double link/image substitution and raise better error messages

    * Bugfix in unittests (include test README file in python package).  Thanks to Wen Heping for reporting this.

* v1.0.3 - 2012-06-11

    * Bugfix: ``AttributeError: 'module' object has no attribute 'interesting_cdata'`` from HTMLParser patch. Thanks to Wen Heping for reporting this.

    * Fix a bug in get_long_description() ReSt test for Py3k and his unittests.

    * Use Travis CI, too.

* v1.0.2 - 2012-04-04

    * Fix "`AttributeError: 'NoneType' object has no attribute 'parent' <https://github.com/jedie/python-creole/issues/6>`_" in html2creole.

* v1.0.1 - 2011-11-16

    * Fix "`TypeError: expected string or buffer <https://github.com/jedie/python-creole/issues/5>`_" in rest2html.

    * `Bugfix in exception handling. <https://github.com/jedie/python-creole/commit/e8422f944709a5f8c2c6a8c8a58a84a92620f035>`_

* v1.0.0 - 2011-10-20

    * Change API: Replace 'parser_kwargs' and 'emitter_kwargs' with separate arguments. (More information on `API Wiki Page <https://github.com/jedie/python-creole/wiki/API>`_)

* v0.9.2

    * Turn zip_safe in setup.py on and change unittests API.

* v0.9.1

    * Many Bugfixes, tested with CPython 2.6, 2.7, 3.2 and PyPy v1.6

* v0.9.0

    * Add Python v3 support (like `http://python3porting.com/noconv.html <http://python3porting.com/noconv.html>`_ strategy)

    * move unittests into creole/tests/

    * Tested with Python 2.7.1, 3.2 and PyPy v1.6.1 15798ab8cf48 jit

* v0.8.5

    * Bugfix in html2creole: ignore links without href

* v0.8.4

    * Bugfix in html parser if list tag has attributes: `https://code.google.com/p/python-creole/issues/detail?id=19#c4 <https://code.google.com/p/python-creole/issues/detail?id=19#c4>`_

* v0.8.3

    * Better error message if given string is not unicode: `https://code.google.com/p/python-creole/issues/detail?id=19 <https://code.google.com/p/python-creole/issues/detail?id=19>`_

* v0.8.2

    * Bugfix in get_long_description() error handling (*local variable 'long_description_origin' referenced before assignment*)

* v0.8.1

    * Bugfix for installation under python 2.5

    * Note: `setup helper <https://github.com/jedie/python-creole/wiki/Use-In-Setup>`_ changed: rename ``GetLongDescription(...)`` to ``get_long_description(...)``

* v0.8

    * New GetLongDescription() helper for setup.py, see: `https://github.com/jedie/python-creole/wiki/Use-In-Setup`_

* v0.7.3

    * Bugfix in html2rest:

        * table without ``<th>`` header

        * new line after table

        * create reference hyperlinks in table cells intead of embedded urls.

        * Don't always use raise_unknown_node()

    * Add child content to raise_unknown_node()

* v0.7.2

    * Activate ``----`` to ``<hr>`` in html2rest

    * Update demo.py

* v0.7.1

    * Bugfix if docutils are not installed

    * API change: rest2html is now here: ``from creole.rest2html.clean_writer import rest2html`` 

* v0.7.0

    * **NEW**: Add a html2reStructuredText converter (only a subset of reSt supported)

* v0.6.1

    * Bugfix: separate lines with one space in "wiki style line breaks" mode

* v0.6

    * **NEW**: html2textile converter

    * some **API changed**!

* v0.5

    * **API changed**:

        * Html2CreoleEmitter optional argument 'unknown_emit' takes now a callable for handle unknown html tags.

        * No macros used as default in creole2html converting.

        * We remove the support for callable macros. Only dict and modules are allowed.

    * remove unknown html tags is default behaviour in html2creole converting.

    * restructure and cleanup sourcecode files.

* v0.4

    * only emit children of empty tags like div and span (contributed by Eric O'Connell)

    * remove inter wiki links and doesn't check the protocol

* v0.3.3

    * Use <tt> when {{{ ... }}} is inline and not <pre>, see: `PyLucid Forum Thread <http://forum.pylucid.org/viewtopic.php?f=3&t=320>`_

    * Bugfix in html2creole: insert newline before new list. TODO: apply to all block tags: `issues 16 <http://code.google.com/p/python-creole/issues/detail?id=16#c5>`_

* v0.3.2

    * Bugfix for spaces after Headline: `issues 15 <https://code.google.com/p/python-creole/issues/detail?id=15>`_

* v0.3.1

    * Make argument 'block_rules' in Parser() optional

* v0.3.0

    * creole2html() has the optional parameter 'blog_line_breaks' to switch from default blog to wiki line breaks

* v0.2.8

    * bugfix in setup.py

* v0.2.7

    * handle obsolete non-closed <br> tag

* v0.2.6

    * bugfix in setup.py

    * Cleanup DocStrings

    * add unittests

* v0.2.5

    * creole2html: Bugfix if "--", "//" etc. stands alone, see also: `issues 12 <http://code.google.com/p/python-creole/issues/detail?id=12>`_

    * Note: bold, italic etc. can't cross line any more.

* v0.2.4

    * creole2html: ignore file extensions in image tag

        * see also: `issues 7 <http://code.google.com/p/python-creole/issues/detail?id=7>`_

* v0.2.3

    * html2creole bugfix/enhanced: convert image tag without alt attribute:

        * see also: `issues 6 <http://code.google.com/p/python-creole/issues/detail?id=6>`_

        * Thanks Betz Stefan alias 'encbladexp'

* v0.2.2

    * html2creole bugfix: convert ``<a href="/url/">Search & Destroy</a>``

* v0.2.1

    * html2creole bugfixes in:

        * converting tables: ignore tbody tag and better handling p and a tags in td

        * converting named entity

* v0.2

    * remove all django template tag stuff: `issues 3 <http://code.google.com/p/python-creole/issues/detail?id=3>`_

    * html code always escaped

* v0.1.1

    * improve macros stuff, patch by Vitja Makarov: `issues 2 <http://code.google.com/p/python-creole/issues/detail?id=2>`_

* v0.1.0

    * first version cut out from `PyLucid CMS <http://www.pylucid.org>`_

.. |^0.15| image:: ^0.15

first source code was written 27.11.2008: `Forum thread (de) <http://www.python-forum.de/viewtopic.php?f=3&t=16742>`_

-------------
Project links
-------------

+--------+------------------------------------------------+
| GitHub | `https://github.com/jedie/python-creole`_      |
+--------+------------------------------------------------+
| Wiki   | `https://github.com/jedie/python-creole/wiki`_ |
+--------+------------------------------------------------+
| PyPi   | `https://pypi.org/project/python-creole/`_     |
+--------+------------------------------------------------+

.. _https://github.com/jedie/python-creole: https://github.com/jedie/python-creole
.. _https://pypi.org/project/python-creole/: https://pypi.org/project/python-creole/

--------
donation
--------

* `paypal.me/JensDiemer <https://www.paypal.me/JensDiemer>`_

* `Flattr This! <https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2Fjedie%2Fpython-creole%2F>`_

* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_

------------

``Note: this file is generated from README.creole 2020-11-04 08:46:39 with "python-creole"``