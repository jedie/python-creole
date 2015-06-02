#!/usr/bin/env python
# coding: utf-8

"""
    unittest for CLI
    ~~~~~~~~~~~~~~~~

    :copyleft: 2013-2015 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import subprocess
import unittest
import sys
import os
import tempfile

from creole.py3compat import PY3
from creole.tests.utils.base_unittest import BaseCreoleTest
from creole import VERSION_STRING


CMDS = ("creole2html", "html2creole", "html2rest", "html2textile")


class CreoleCLITests(BaseCreoleTest):
    CMD_PATH = None

    @classmethod
    def setUpClass(cls):
        # FIXME: How can this be easier?!?
        prog = CMDS[0]
        cls.CMD_PATH = os.path.abspath(os.path.dirname(sys.executable))
        if not os.path.isfile(os.path.join(cls.CMD_PATH, prog)):
            for path in sys.path:
                if os.path.isfile(os.path.join(path, prog)):
                    cls.CMD_PATH = path
                    break

    def _subprocess(self, popen_args, verbose=True):
        assert isinstance(popen_args, list)

        # set absolute path to called cli program
        prog = popen_args[0]
        prog = os.path.join(self.CMD_PATH, prog)
        self.assertTrue(os.path.isfile(prog), "File not found: %r" % prog)
        self.assertTrue(os.access(prog, os.X_OK), "File %r is not executeable?!?" % prog)
        popen_args[0] = prog

        if verbose:
            print("Call:", popen_args)

        process = subprocess.Popen(popen_args,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        stdout, stderr = process.communicate()
        retcode = process.poll()

        if verbose:
            print("return code: %r" % retcode)
            print("stdout: %r" % stdout)
            print("stderr: %r" % stderr)

        stdout = stdout.strip()
        stderr = stderr.strip()
        return popen_args, retcode, stdout, stderr

    def assertSubprocess(self, popen_args, retcode, stdout, stderr, verbose=True):
        popen_args2, retcode2, stdout2, stderr2 = self._subprocess(popen_args, verbose)
        try:
            self.assertEqual(stdout, stdout2, "stdout wrong:")
            self.assertEqual(stderr, stderr2, "stderr wrong:")
            self.assertEqual(retcode, retcode2, "return code wrong:")
        except AssertionError as err:
            msg = (
                "Error: %s"
                "call via subprocess: %s\n"
                "return code........: %r\n"
                " ---------- [stdout] ---------- \n"
                "%s\n"
                " ---------- [stderr] ---------- \n"
                "%s\n"
                "-------------------------------"
            ) % (
                err,
                repr(popen_args2), retcode2,
                stdout2, stderr2,
            )
            self.fail(msg)

    def _test_convert(self, source_content, dest_content, cli_str, verbose=True):
        assert isinstance(source_content, bytes), type(source_content)
        assert isinstance(dest_content, bytes), type(dest_content)

        source_file = tempfile.NamedTemporaryFile()
        sourcefilepath = source_file.name
        source_file.write(source_content)
        source_file.seek(0)

        dest_file = tempfile.NamedTemporaryFile()
        destfilepath = dest_file.name

        stdout=(
            "Convert '%(src)s' to '%(dst)s' with %(prog)s (codec: utf-8)\n"
            "done. '%(dst)s' created."
        ) % {
            "prog": cli_str,
            "src": sourcefilepath,
            "dst": destfilepath,
        }

        self.assertSubprocess(
            popen_args=[cli_str, sourcefilepath, destfilepath],
            retcode=0, stdout=stdout, stderr="",
            verbose=False,
        )

        dest_file.seek(0)
        result_content = dest_file.read()

        result_content = result_content.decode("utf-8")
        dest_content = dest_content.decode("utf-8")
        self.assertEqual(result_content, dest_content)

    def test_version(self):
        for cmd in CMDS:
            version_info = "%s from python-creole v%s" % (
                cmd, VERSION_STRING
            )
            if PY3:
                self.assertSubprocess(
                    popen_args=[cmd, "--version"],
                    retcode=0,
                    stdout=version_info,
                    stderr="",
                    verbose=False,
                )
            else:
                self.assertSubprocess(
                    popen_args=[cmd, "--version"],
                    retcode=0,
                    stdout="",
                    stderr=version_info,
                    verbose=False,
                )

    def test_creole2html(self):
        self._test_convert(
            source_content=b"= test creole2html =",
            dest_content=b"<h1>test creole2html</h1>",
            cli_str="creole2html",
        )

    def test_html2creole(self):
        self._test_convert(
            source_content=b"<h1>test html2creole</h1>",
            dest_content=b"= test html2creole",
            cli_str="html2creole",
        )

    def test_html2rest(self):
        self._test_convert(
            source_content=b"<h1>test html2rest</h1>",
            dest_content=(b"==============\n"
                          b"test html2rest\n"
                          b"=============="
            ),
            cli_str="html2rest",
        )

    def test_html2textile(self):
        self._test_convert(
            source_content=b"<h1>test html2textile</h1>",
            dest_content=b"h1. test html2textile",
            cli_str="html2textile",
        )


if __name__ == '__main__':
    unittest.main()
