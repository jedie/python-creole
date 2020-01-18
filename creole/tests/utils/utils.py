# coding: utf-8


"""
    unitest generic utils
    ~~~~~~~~~~~~~~~~~~~~~

    Generic utils useable for a markup test.

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import difflib
import textwrap
import unittest

# error output format:
# =1 -> via repr()
# =2 -> raw
VERBOSE = 1
#VERBOSE = 2


def make_diff(block1, block2):
    d = difflib.Differ()

    block1 = block1.replace("\\n", "\\n\n").split("\n")
    block2 = block2.replace("\\n", "\\n\n").split("\n")

    diff = d.compare(block1, block2)

    result = ["%2s %s\n" % (line, i) for line, i in enumerate(diff)]
    return "".join(result)


class MarkupTest(unittest.TestCase):
    """
    Special error class: Try to display markup errors in a better way.
    """

    def _format_output(self, txt):
        txt = txt.split("\\n")
        if VERBOSE == 1:
            txt = "".join(['%s\\n\n' % i for i in txt])
        elif VERBOSE == 2:
            txt = "".join(['%s\n' % i for i in txt])
        return txt

    def assertEqual(self, first, second, msg=""):
        if first == second:
            return

        try:
            diff = make_diff(first, second)
        except AttributeError:
            raise self.failureException(f"{first!r} is not {second!r}")

        print("*" * 100)
        print("---[Output:]-----------------------------------------------------------------------------------------")
        print(first)
        print("---[not equal to:]-----------------------------------------------------------------------------------")
        print(second)
        print("---[diff:]-------------------------------------------------------------------------------------------")
        print(diff)
        print("*" * 100)

        assert first == second, f"{first!r} is not {second!r}"

    def _prepare_text(self, txt):
        """
        prepare the multiline, indentation text.
        """
        # Remove any common leading whitespace from every line
        txt = textwrap.dedent(txt)

        # Strip spaces and every line end and remove the last line ending:
        txt = "\n".join(line.rstrip(" ") for line in txt.splitlines())

        # strip *one* newline at the beginning...
        if txt.startswith("\n"):
            txt = txt[1:]

        return txt
