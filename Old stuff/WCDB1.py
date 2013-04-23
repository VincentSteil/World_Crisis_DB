# -------------------
# WCDB1.py
# Group project
# Lab 3
# -------------------

# -------------
# imports
# -------------

import sys
import xml.etree.ElementTree as ET
from cStringIO import StringIO

# -------------
# WCDB_print
# -------------

def WCDB1_print(w, tree):
  """
  This function prints tree to writer w
  w is a writer
  tree is a string to print
  """
  w.write(tree) #printing to .out file

# -------------
# WCDB1_run
# -------------

  
def WCDB1_run(r ,w):
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
