# coding: utf-8

"""
    unittest subprocess helper
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2015 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""



import json
import os
import subprocess
import sys


class SubprocessMixin(object):
    # call .../env/bin/python will not add the .../env/bin/ to the PATH
    SEARCH_PATH = [os.path.dirname(sys.executable)] + os.environ.get("PATH", "").split(os.pathsep)

    def find_executable(self, program):
        self.assertNotIn(os.sep, program)
        for path in self.SEARCH_PATH:
            filepath = os.path.join(path, program)
            if os.path.isfile(filepath):
                if not os.access(filepath, os.X_OK):
                    sys.stderr.write(f"File {filepath!r} is not executable?!?\n")
                else:
                    return filepath

        self.fail("Program %s not found in:\n\t* %s" % (json.dumps(program), "\n\t* ".join(self.SEARCH_PATH)))

    def subprocess(self, popen_args, verbose=True):
        assert isinstance(popen_args, (tuple, list))

        if verbose:
            print("Call:", popen_args)

        try:
            process = subprocess.Popen(
                popen_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
            )
        except Exception as err:
            self.fail(f"Error subprocess call with {popen_args!r}: {err}")

        stdout, stderr = process.communicate()
        retcode = process.poll()

        if verbose:
            print(f"return code: {retcode!r}")
            print(f"stdout: {stdout!r}")
            print(f"stderr: {stderr!r}")

        stdout = stdout.strip()
        return popen_args, retcode, stdout

    def assertSubprocess(self, popen_args, retcode, stdout, verbose=True):
        popen_args2, retcode2, stdout2 = self.subprocess(popen_args, verbose)
        stdout = stdout.strip()
        try:
            self.assertEqual(stdout, stdout2, "stdout wrong:")
            self.assertEqual(retcode, retcode2, "return code wrong:")
        except AssertionError as err:
            msg = (
                "Error: %s"
                "call via subprocess: %s\n"
                "return code........: %r\n"
                " ---------- [stdout] ---------- \n"
                "%s\n"
                "-------------------------------"
            ) % (err, repr(popen_args2), retcode2, stdout2,)
            self.fail(msg)
