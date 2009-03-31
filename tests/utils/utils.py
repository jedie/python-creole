# -*- coding: utf-8 -*-

"""
    unitest generic utils
    ~~~~~~~~~~~~~~~~~~~~~

    Generic utils useable for a markup test.

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate:$
    $Rev:$
    $Author$

    :copyleft: 2008-2009 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE.txt for more details.
"""

import sys
import difflib
import unittest
import traceback


## error output format:
# =1 -> via repr()
# =2 -> raw
#VERBOSE = 1
VERBOSE = 2


class MarkupDiffFailure(Exception):
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

    def _diff(self, block1, block2):
        d = difflib.Differ()

        block1 = block1.replace("\\n", "\\n\n").split("\n")
        block2 = block2.replace("\\n", "\\n\n").split("\n")

        diff = d.compare(block1, block2)

        result = ["%2s %s\n" % (line, i) for line, i in enumerate(diff)]
        return "".join(result)

    def _split_message(self, raw_msg):
        """
        Get the right split_string is not easy. There are many variants. Every
        part of the string can be used ' oder " and can be marked with the
        'u' (unicode) character.
        Here some tests:

        >>> MarkupDiffFailure()._split_message('''"foo" != "bar"''')
        ('foo', 'bar')

        >>> MarkupDiffFailure()._split_message('''u"foo" != "bar"''')
        ('foo', 'bar')
        >>> MarkupDiffFailure()._split_message('''"foo" != u"bar"''')
        ('foo', 'bar')
        >>> MarkupDiffFailure()._split_message('''u"foo" != u"bar"''')
        ('foo', 'bar')
        >>> MarkupDiffFailure()._split_message('''u'foo' != "bar"''')
        ('foo', 'bar')
        >>> MarkupDiffFailure()._split_message(''''foo' != u"bar"''')
        ('foo', 'bar')

        >>> MarkupDiffFailure()._split_message('''u"" != u"bar"''')
        ('', 'bar')
        >>> MarkupDiffFailure()._split_message('''u'foo' != u""''')
        ('foo', '')

        With and without a 'u' ;)
        """
#        print repr(raw_msg)

        msg = raw_msg.lstrip("u")
#        print repr(msg)

        first_quote = msg[0]
        second_quote  = msg[-1]
        #print "quote chars: [%s] [%s]" % (first_quote, second_quote)

        split_string = "%s != %s" % (first_quote, second_quote)
        #print "split string1:", split_string

        if split_string not in msg:
            # Second part is unicode?
            split_string = "%s != u%s" % (first_quote, second_quote)
            #print "split string2:", split_string

        if split_string not in msg:
            msg = (
                "Split error output failed!"
                " - split string >%s< not in message: %s"
            ) % (split_string, raw_msg)
            raise AssertionError(msg)

        try:
            block1, block2 = msg.split(split_string)
        except ValueError, err:
            msg = self._format_output(msg)
            return (
                "Can't split error output: %r\n"
                "Info:\n%s\n"
                "raw split: %r"
            ) % (err, msg, msg.split(split_string))

        block1 = block1.strip("'\"")
        block2 = block2.strip("'\"")

        return block1, block2

    def _build_errormsg(self):
        raw_msg = self.args[0]

        """

        """
        block1, block2 = self._split_message(raw_msg)


        #~ block1 = block1.rstrip("\\n")
        #~ block2 = block2.rstrip("\\n")
        diff = self._diff(block1, block2)

        block1 = self._format_output(block1)
        block2 = self._format_output(block2)

        return (
            "%r\n\n---[Output:]---\n%s\n"
            "---[not equal to:]---\n%s"
            "\n---[diff:]---\n%s"
        ) % (raw_msg, block1, block2, diff)

    def __str__(self):
        try:
            return self._build_errormsg()
        except:
            etype, value, tb = sys.exc_info()
            return traceback.format_exc(tb)




class MarkupTest(unittest.TestCase):

    # Use the own error class from above
    failureException = MarkupDiffFailure

    def _prepare_text(self, txt):
        """
        prepare the multiline, indentation text.
        """
        txt = unicode(txt)
        txt = txt.splitlines()
        assert txt[0]=="", "First must be empty!"
        txt = txt[1:] # Skip the first line

        # get the indentation level from the first line
        count = False
        for count, char in enumerate(txt[0]):
            if char!=" ":
                break

        assert count != False, "second line is empty!"

        # remove indentation from all lines
        txt = [i[count:].rstrip(" ") for i in txt]

        #~ txt = re.sub("\n {2,}", "\n", txt)
        txt = "\n".join(txt)

        # strip *one* newline at the begining...
        if txt.startswith("\n"): txt = txt[1:]
        # and strip *one* newline at the end of the text
        if txt.endswith("\n"): txt = txt[:-1]
        #~ print repr(txt)
        #~ print "-"*79

        return txt

    def testSelf(self):
        """
        Test for self._prepare_text()
        """
        out1 = self._prepare_text("""
            one line
            line two""")
        self.assertEqual(out1, "one line\nline two")

        out2 = self._prepare_text("""
            one line
            line two
        """)
        self.assertEqual(out2, "one line\nline two")

        out3 = self._prepare_text("""
            one line

            line two
        """)
        self.assertEqual(out3, "one line\n\nline two")

        out4 = self._prepare_text("""
            one line
                line two

        """)
        self.assertEqual(out4, "one line\n    line two\n")

        # removing whitespace and the end
        self.assertEqual(self._prepare_text("\n  111  \n  222"), "111\n222")

        out5 = self._prepare_text("""
            one line
                line two
            dritte Zeile
        """)
        self.assertEqual(out5, "one line\n    line two\ndritte Zeile")

        self.assertRaises(
            MarkupDiffFailure, self.assertEqual, "foo", "bar"
        )



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print "doc test done."

    unittest.main()