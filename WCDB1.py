"""
WCDB1.py
Group project
Lab 3
"""

import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml') #where to import from
root = tree.getroot()
print root;
tree.write('bum.xml') # where to export to
