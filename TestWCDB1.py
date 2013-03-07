# -------------------
# TestWCDB1.py
# Lab 3
# Group project
# -------------------

# imports

import StringIO
import unittest

from WCDB1 import WCDB1_run, WCDB1_print

# -----------
# TestXML
# -----------

class TestWCDB1 (unittest.TestCase) :
    # ----
    # run
    # ----

    def test_run1 (self) :
        r = StringIO.StringIO('<one>\n</one>')
        w = StringIO.StringIO('')
        WCDB1_run(r, w)
        self.assert_(r.getvalue() == w.getvalue())

    def test_run2 (self) :
        r = StringIO.StringIO("<country name=\"Liechtenstein\">\n<rank>1</rank>\n<year>2008</year>\n</country>")
        w = StringIO.StringIO('')
        WCDB1_run(r, w)
        self.assert_(r.getvalue() == w.getvalue())
        
    def test_run3 (self) :
        r = StringIO.StringIO("<book id=\"bk101\">\n<author>Gambardella, Matthew</author>\n<title>\nXML Developer's Guide\n</title><genre>Computer</genre><price>44.95</price><publish_date>2000-10-01</publish_date><description>An in-depth look at creating applicationswith XML.</description></book>")
        w = StringIO.StringIO('')
        WCDB1_run(r, w)
        self.assert_(r.getvalue() == w.getvalue())

    # ----
    # print
    # ----

    def test_print1 (self) :
        r = "abc"
        w = StringIO.StringIO('')
        WCDB1_print(w, r)
        self.assert_(r == w.getvalue())

    def test_print2 (self) :
        r = "Test\n"
        w = StringIO.StringIO('')
        WCDB1_print(w, r)
        self.assert_(r == w.getvalue())
        
    def test_print3 (self) :
        r = "This is a long sentence. Hey!\n And another one! \n"
        w = StringIO.StringIO('')
        WCDB1_print(w, r)
        self.assert_(r == w.getvalue())

# ----
# main
# ----

print "TestWCDB1.py"
unittest.main()
print "Done."
