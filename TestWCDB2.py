# -------------------
# TestWCDB2.py
# Lab 3
# Group project
# -------------------

# imports

import StringIO
import unittest
import sys
import xml.etree.ElementTree as ET
from cStringIO import StringIO
import _mysql
import ast
import xml.dom.minidom

from WCDB2 import WCDB2_run, WCDB2_print, login, query, WCDB2_setup, WCDB2_import, WCDB2_export

# -----------
# TestXML
# -----------

class TestWCDB2 (unittest.TestCase) :
    
    # ----------------------------------------------
    # No unit tests for login and query since these functions are taken from Course website.
    # ----------------------------------------------

    # ----
    # WCDB2_setup
    # ----

    def test_setup1 (self) :
        c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
        WCDB2_setup(c)
        self.assert_(str(type(c)) == "<type '_mysql.connection'>")

    def test_setup2 (self) :
        c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
        WCDB2_setup(c)
        self.assert_(str(type(c)) == "<type '_mysql.connection'>")
        
    def test_setup3 (self) :
        c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
        WCDB2_setup(c)
        self.assert_(str(type(c)) == "<type '_mysql.connection'>")

    # -------------
    # WCDB2_import
    # -------------
    
    def test_import1 (self) :
        c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
        tree = ET.parse(StringIO("<Bar><PersonKind id=\"1\"><Name>Cela</Name></PersonKind><Person id=\"12\"><Name><Suffix>Waza</Suffix></Name></Person><Organization hcwd=\"45\"><Location><Locality>Austin</Locality></Location><ContactInfo><PostalAddress><Locality>Marchew</Locality></PostalAddress></ContactInfo></Organization><Crisis bazyl=\"123\"><Kind va=\"12\"/><StartDateTime><Date>34</Date></StartDateTime></Crisis><Crisis bazyl=\"0\"><Name>Cela</Name><Location><Locality>Austin</Locality></Location><Location><Locality>Boston</Locality><Country>USA</Country></Location><ExternalResources><ImageURL>www</ImageURL><VideoURL>d</VideoURL><ImageURL>ccc</ImageURL></ExternalResources><StartDateTime><Date>34</Date><Time>33</Time></StartDateTime></Crisis></Bar>")) #importing the XML
        root = tree.getroot()
        WCDB2_setup(c)
        WCDB2_import(c, root)
        self.assert_(len(query(c, "select * from Crises;"))>0)

    def test_import2 (self) :
        c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
        tree = ET.parse(StringIO("<Bar><PersonKind id=\"1\"><Name>Cela</Name></PersonKind><Person id=\"12\"><Name><Suffix>Waza</Suffix></Name></Person><Person id=\"7\"><Name><FirstName>Kozak</FirstName></Name></Person><Organization hcwd=\"45\"><Location><Locality>Austin</Locality></Location><ContactInfo><PostalAddress><Locality>Marchew</Locality></PostalAddress></ContactInfo></Organization><Crisis bazyl=\"123\"><Kind va=\"12\"/><StartDateTime><Date>34</Date></StartDateTime></Crisis><Crisis bazyl=\"0\"><Name>Cela</Name><Location><Locality>Austin</Locality></Location><Location><Locality>Boston</Locality><Country>USA</Country></Location><ExternalResources><ImageURL>www</ImageURL><VideoURL>d</VideoURL><ImageURL>ccc</ImageURL></ExternalResources><StartDateTime><Date>34</Date><Time>33</Time></StartDateTime></Crisis></Bar>")) #importing the XML
        root = tree.getroot()
        WCDB2_setup(c)
        WCDB2_import(c, root)
        self.assert_(len(query(c, "select * from Persons;"))==2)
        
    def test_import3 (self) :
        c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
        tree = ET.parse(StringIO("<WorldCrises></WorldCrises>"))
        root = tree.getroot()
        WCDB2_setup(c)
        WCDB2_import(c, root)
        self.assert_(len(query(c, "select * from Organizations;"))==0)

    # -------------
    # WCDB2_export
    # -------------
    
    def test_export1 (self) :
        c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
        a=WCDB2_export(c)
        self.assert_(a is not None)

    def test_export2 (self) :
        c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
        a=WCDB2_export(c)
        self.assert_(a.tag == "WorldCrises")
        
    def test_export3 (self) :
        c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
        a=WCDB2_export(c)
        self.assert_(str(type(a))=="<class 'xml.etree.ElementTree.Element'>")
        
    # ----
    # run
    # ----

    def test_run1 (self) :
        import StringIO
        r = StringIO.StringIO('<WorldCrises>\n</WorldCrises>\n')
        w = StringIO.StringIO('')
        WCDB2_run(r, w)
        self.assert_("<?xml version=\"1.0\" ?>\n<WorldCrises/>\n" == w.getvalue())

    def test_run2 (self) :
        import StringIO
        r = StringIO.StringIO('<WorldCrises>\n<x></x></WorldCrises>\n')
        w = StringIO.StringIO('')
        WCDB2_run(r, w)
        self.assert_("<?xml version=\"1.0\" ?>\n<WorldCrises/>\n" == w.getvalue())
        
    def test_run3 (self) :
        import StringIO
        r = StringIO.StringIO('<WorldCrises>\n<CrisisKind id=\"3\"></CrisisKind></WorldCrises>\n')
        w = StringIO.StringIO('')
        WCDB2_run(r, w)
        self.assert_("<?xml version=\"1.0\" ?>\n<WorldCrises>\n\t<CrisisKind crisisKindIdent=\"3\">\n\t\t<Name/>\n\t\t<Description/>\n\t</CrisisKind>\n</WorldCrises>\n" == w.getvalue())

    # ----
    # print
    # ----
    def test_print1 (self) :
        import StringIO
        r = "<abc></abc>"
        w = StringIO.StringIO('')
        WCDB2_print(w, r)
        self.assert_("<?xml version=\"1.0\" ?>\n<abc/>\n" == w.getvalue())

    def test_print2 (self) :
        import StringIO
        r = "<abc j=\"2\"></abc>"
        w = StringIO.StringIO('')
        WCDB2_print(w, r)
        self.assert_("<?xml version=\"1.0\" ?>\n<abc j=\"2\"/>\n" == w.getvalue())
        
    def test_print3 (self) :
        import StringIO
        r = "<abc><x></x></abc>"
        w = StringIO.StringIO('')
        WCDB2_print(w, r)
        self.assert_("<?xml version=\"1.0\" ?>\n<abc>\n\t<x/>\n</abc>\n" == w.getvalue())

# ----
# main
# ----

print "TestWCDB2.py"
unittest.main()
print "Done."
