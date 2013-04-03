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
  """
  This function gets the login info and logins to a MySQL database
  c is a mysql connection
  """
  in1 = raw_input('Host: ')
  in2 = raw_input('Username: ')
  in3 = raw_input('Password: ')
  in4 = raw_input('Database: ')
  c = _mysql.connect(
          host = in1,
          user = in2,
          passwd = in3,
          db = in4)
  assert str(type(c)) == "<type '_mysql.connection'>"
  print "OK connection"
  return c

# -------------
# query
# -------------

def query (c, s) :
  """
  This function executes a query and returns its result
  c is a mysql connection
  s is a string that contains the query
  t is the result/outcome of the query to be returned
  """
  
  assert str(type(c)) == "<type '_mysql.connection'>"
  assert type(s) is str
  c.query(s)
  r = c.use_result()
  if r is None :
      return None
  assert str(type(r)) == "<type '_mysql.result'>"
  t = r.fetch_row(maxrows = 0)
  assert type(t) is tuple
  return t
  

# -------------
# WCDB_setup
# -------------

def WCDB2_setup(c):
  """
  This function sets up the MySQL database that we will use
  c is a mysql connection
  """
                #makes sure tables are deleted
  t = Query.query(c, "drop table if exists Crises;")
  assert t is None
                #creates a table
  t = query(c, """    
    create table Crises (
    sID text,
    sName text,
    Kind text,
    Loc text,
    SDT text, EDT text, HI text, EI text, RN text, WTH text, ER text, RP text, RO text);
  """)
  assert t is None

# -------------
# WCDB_import
# -------------

def WCDB2_import(c, root):
  """
  This function sets up the MySQL database that we will use
  c is a mysql connection
  tree is an ElementTree
  """
  for crisis in root.findall('Crisis'):
    tup = {"ID" : "", "Name" : "", "Kind" : "", "Location" : [], "StartDateTime" : "", "EndDateTime" : "",
           "HumanImpact" : [], "EconomicImpact" : "", "ResourceNeeded" : [], "WaysToHelp" : [], "ExternalResources" : "",
           "RelatedPersons" : [], "RelatedOrganizations" : []}
    tup["ID"]=j.attrib.keys()[0]
    for i in crisis :
      if len(i) == 0 :
        tup[i.tag]+=i.text
      elif i.tag=="Location":
        tup["Location"]+=[i.find("Locality").text, i.find("Region").text, i.find("Country").text]
      elif i.tag=="StartDateTime" or i.tag=="EndDateTime":
        tup[i.tag]=[i.find("Date").text, i.find("Time").text]
      elif i.tag=="HumanImpact":
        tup[i.tag]+=[i.find("Type").text, i.find("Number").text]
      elif i.tag=="ExternalResources":
        tup[i.tag]=[]
        for j in i.iter():
          tup[i.tag]+=[j.tag, j.text]
      elif i.tag=="RelatedPersons" or i.tag=="RelatedOrganizations":
        tup[i.tag]=[]
        for j in i.iter():
          tup[i.tag]+=j.attrib.keys()[0]
  query(c, "insert into Crises values " + str(tuple(tup.values())) + ";")

  for crisis in root.findall('Organization'):
    tup = {"ID" : "", "Name" : "", "Kind" : "", "Location" : "", "History" : "", "Telephone" : "",
           "Fax" : "", "Email" : "", "StreetAddress" : "", "Locality" : "", "Region" : "",
           "PostalCode" : "", "Country" : "", "ExternalResources" : "", "RelatedPersons" : "", "RelatedCrises" : ""}
  query(c, "insert into Student values (123, 'Amy', 3.9, 1000);")    

  for crisis in root.findall('Person'):
    tup = {"ID" : "", "FirstName" : "", "MiddleName" : "", "LastName" : "", "Suffix" : "", "Kind" : "", "Location" : "",
           "RelatedCrises" : "", "RelatedOrganizations" : ""}
  query(c, "insert into Student values (123, 'Amy', 3.9, 1000);")

  for crisis in root.findall('CrisisKind'):
    tup = {"ID" : "", "Name" : "", "Description" : ""}
  query(c, "insert into Student values (123, 'Amy', 3.9, 1000);")

  for crisis in root.findall('OrganizationKind'):
    tup = {"ID" : "", "Name" : "", "Description" : ""}
  query(c, "insert into Student values (123, 'Amy', 3.9, 1000);")

  for crisis in root.findall('PersonKind'):
    tup = {"ID" : "", "Name" : "", "Description" : ""}
  query(c, "insert into Student values (123, 'Amy', 3.9, 1000);")

# -------------
# WCDB_export
# -------------

def WCDB2_export(c):
  """
  This function sets up the MySQL database that we will use
  c is a mysql connection
  """
                #makes sure tables are deleted
  t = Query.query(c, "drop table if exists Student;")
  assert t is None
                #creates a table
  t = query(c, """    
            
  """)
  assert t is None

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
