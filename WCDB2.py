# -------------------
# WCDB2.py
# Group name: Is Yuchen Here Today?
# Lab 4
# -------------------

# -------------
# imports
# -------------

import sys
import xml.etree.ElementTree as ET
from cStringIO import StringIO
import _mysql

# -------------
# login
# -------------

def login () :
    in1 = raw_input('Host: ')
    in2 = raw_input('Username: ')
    in3 = raw_input('Password: ')
    in4 = raw_input('Database: ')
    c = _mysql.connect(
            host = "z",
            user = "<username>",
            passwd = "<password>",
            db = "downing_test")
    assert str(type(c)) == "<type '_mysql.connection'>"
    print "OK connection"
    return c

# -------------
# WCDB_print
# -------------

def WCDB2_print(w, tree):
  """
  This function prints tree to writer w
  w is a writer
  tree is a string to print
  """
  w.write(tree) #printing to .out file

# -------------
# WCDB2_run
# -------------

  
def WCDB2_run(r ,w):
  """
  This function reads from the input and prints to input an XML
  r is a reader
  w is a writer
  """

  strr = r.read()
  assert len(strr)>0
  tree = ET.parse(StringIO(strr)) #importing the XML
  root = tree.getroot()
  WCDB1_print(w, ET.tostring(root)) #sending tree to the printer

login()
