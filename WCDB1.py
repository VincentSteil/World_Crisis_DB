"""
WCDB1.py
Group project
Lab 3
"""
import sys
import xml.etree.ElementTree as ET
from cStringIO import StringIO


def WCBD_print(w, tree):
  w.write(tree) #printing to .out file
  
def WCDB1_run(r ,w):
  """
  r is a reader
  w is a writer
  """
 
  strr = r
  tree = ET.parse(strr) #importing the XML
  root = tree.getroot()
  WCBD_print(w, ET.tostring(root)) #sending tree to the printer
