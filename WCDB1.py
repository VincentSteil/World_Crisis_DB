"""
WCDB1.py
Group project
Lab 3
"""
import sys
import xml.etree.ElementTree as ET
from cStringIO import StringIO
strr = sys.stdin.read()
tree = ET.parse(StringIO(strr)) #importing the XML
root = tree.getroot()
print ET.tostring(root) #printing the result to the console
