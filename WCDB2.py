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
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
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
# WCDB2_setup
# -------------

def WCDB2_setup(c):
  """
  This function sets up the MySQL database that we will use
  c is a mysql connection
  """
                #makes sure tables are deleted
  t = query(c, "drop table if exists Crises;")
  assert t is None
  t = query(c, "drop table if exists Organizations;")
  assert t is None
  t = query(c, "drop table if exists Persons;")
  assert t is None
  t = query(c, "drop table if exists CrisisKinds;")
  assert t is None
  t = query(c, "drop table if exists PersonKinds;")
  assert t is None
  t = query(c, "drop table if exists OrgKinds;")
  assert t is None
                #creates a table
  t = query(c, """    
    create table Crises (
    cID text,
    cName text,
    cKind text,
    Loc text,
    SDT text, EDT text, HI text, EI text, RN text, WTH text, ER text, RP text, RO text);
  """)

  t = query(c, """    
    create table Organizations (
    oID text,
    oName text,
    oKind text,
    Loc text,
    Hist text, Tel text, Fax text, Email text, St text, Locl text, Reg text, ZIP text, CTR text, ER text, RP text, RC text);
  """)

  t = query(c, """    
    create table Persons (
    pID text,
    FName text,
    MName text,
    LName text,
    Sfx text, pKind text, Loc text, ER text, RO text, RC text);
  """)
  
  t = query(c, """    
    create table CrisisKinds (
    cKind text,
    Name text,
    Dscr text );
  """)
  t = query(c, """    
    create table OrgKinds (
    oKind text,
    Name text,
    Dscr text );
  """)
  t = query(c, """    
    create table PersonKinds (
    pKind text,
    Name text,
    Dscr text );
  """)
  assert t is None

# -------------
# WCDB2_import
# -------------

def WCDB2_import(c, root):
  """
  This function sets up the MySQL database that we will use
  c is a mysql connection
  tree is an ElementTree
  """
  #Crises
  for crisis in root.findall('Crisis'):
    tup = {"ID" : "", "Name" : "", "Kind" : "", "Location" : [], "StartDateTime" : "", "EndDateTime" : "",
           "HumanImpact" : [], "EconomicImpact" : "", "ResourceNeeded" : [], "WaysToHelp" : [], "ExternalResources" : "",
           "RelatedPersons" : [], "RelatedOrganizations" : []}
    ordering = ["ID", "Name", "Kind", "Location", "StartDateTime", "EndDateTime",
           "HumanImpact", "EconomicImpact", "ResourceNeeded", "WaysToHelp", "ExternalResources",
           "RelatedPersons", "RelatedOrganizations"]
    tup["ID"]=crisis.attrib.values()[0]
    
    for i in crisis :
      if i.tag=="Kind":
        tup["Kind"]=i.attrib.values()[0]
      elif len(i) == 0 :
        tup[i.tag]+=i.text
      elif i.tag=="Location":
        temp=dict()
        for j in i.iter():
          temp[j.tag]=j.text
        del temp["Location"]
        tup[i.tag].append(temp)
      elif i.tag=="StartDateTime" or i.tag=="EndDateTime":
        if i.find("Time") != None :
          tup[i.tag]=[i.find("Date").text, i.find("Time").text]
        else:
          tup[i.tag]=[i.find("Date").text, ""]
      elif i.tag=="HumanImpact":
        tup[i.tag]+=[i.find("Type").text, i.find("Number").text]
      elif i.tag=="ExternalResources":
        tup[i.tag]=[]
        for j in i.iter():
          if j.tag!=i.tag:
            tup[i.tag]+=[[j.tag, j.text]]
      elif i.tag=="RelatedPersons" or i.tag=="RelatedOrganizations":
        tup[i.tag]=[]
        for j in i.iter():
          if j.tag!=i.tag:
            tup[i.tag]+=j.attrib.values()[0]
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    print str(tuple(ret))
    query(c, "insert into Crises values " + str(tuple(ret)) + ";")
  
   #Orgs
  for crisis in root.findall('Organization'):
    tup = {"ID" : "", "Name" : "", "Kind" : "", "Location" : [], "History" : "", "Telephone" : "",
           "Fax" : "", "Email" : "", "StreetAddress" : "", "Locality" : "", "Region" : "",
           "PostalCode" : "", "Country" : "", "ExternalResources" : "", "RelatedPersons" : [], "RelatedCrises" : []}
    ordering = ["ID", "Name", "Kind", "Location", "History", "Telephone",
           "Fax", "Email", "StreetAddress", "Locality", "Region",
           "PostalCode", "Country", "ExternalResources", "RelatedPersons", "RelatedCrises"]
    tup["ID"]=crisis.attrib.values()[0]
    
    for i in crisis :
      if i.tag=="Kind":
        tup["Kind"]=i.attrib.values()[0]
      elif len(i) == 0 :
        tup[i.tag]+=i.text
      elif i.tag=="Location":
        temp=dict()
        for j in i.iter():
          temp[j.tag]=j.text
        del temp["Location"]
        tup[i.tag].append(temp)
      elif i.tag=="ContactInfo":
        for j in i.iter():
          tup[j.tag]=j.text
        del tup["ContactInfo"]
        del tup["PostalAddress"]
      elif i.tag=="ExternalResources":
        tup[i.tag]=[]
        for j in i.iter():
          if j.tag!=i.tag:
            tup[i.tag]+=[[j.tag, j.text]]
      elif i.tag=="RelatedPersons" or i.tag=="RelatedCrises":
        tup[i.tag]=[]
        for j in i.iter():
          if j.tag!=i.tag:
            tup[i.tag]+=j.attrib.values()[0]
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    print str(tuple(ret))
    query(c, "insert into Organizations values " + str(tuple(ret)) + ";")  
    #persons
  for crisis in root.findall('Person'):
    tup = {"ID" : "", "FirstName" : "", "MiddleName" : "", "LastName" : "", "Suffix" : "", "Kind" : "", "Location" : [],
           "ExternalResources" : "", "RelatedCrises" : [], "RelatedOrganizations" : []}
    ordering = ["ID", "FirstName", "MiddleName", "LastName", "Suffix", "Kind", "Location", "ExternalResources",
           "RelatedCrises", "RelatedOrganizations"]
    tup["ID"]=crisis.attrib.values()[0]
    
    for i in crisis :
      if i.tag=="Kind":
        tup["Kind"]=i.attrib.values()[0]
      elif len(i) == 0 :
        tup[i.tag]+=i.text
      elif i.tag=="Location":
        temp=dict()
        for j in i.iter():
          temp[j.tag]=j.text
        del temp["Location"]
        tup[i.tag].append(temp)
      elif i.tag=="Name":
        for j in i.iter():
          tup[j.tag]=j.text
        del tup["Name"]
      elif i.tag=="ExternalResources":
        tup[i.tag]=[]
        for j in i.iter():
          if j.tag!=i.tag:
            tup[i.tag]+=[[j.tag, j.text]]
      elif i.tag=="RelatedOrganizations" or i.tag=="RelatedCrises":
        tup[i.tag]=[]
        for j in i.iter():
          if j.tag!=i.tag:
            tup[i.tag]+=j.attrib.values()[0]
    
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    print str(tuple(ret))
    query(c, "insert into Persons values " + str(tuple(ret)) + ";")
  
  for crisis in root.findall('CrisisKind'):
    tup = {"ID" : "", "Name" : "", "Description" : ""}
    ordering = ["ID", "Name", "Description"]
    tup["ID"]=crisis.attrib.values()[0]
    for i in crisis :
      tup[i.tag]+=i.text
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    print str(tuple(ret))
    query(c, "insert into CrisisKinds values " + str(tuple(ret)) + ";")

  for crisis in root.findall('OrganizationKind'):
    tup = {"ID" : "", "Name" : "", "Description" : ""}
    ordering = ["ID", "Name", "Description"]
    tup["ID"]=crisis.attrib.values()[0]
    for i in crisis :
      tup[i.tag]+=i.text
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    print str(tuple(ret))
    query(c, "insert into OrgKinds values " + str(tuple(ret)) + ";")

  for crisis in root.findall('PersonKind'):
    tup = {"ID" : "", "Name" : "", "Description" : ""}
    ordering = ["ID", "Name", "Description"]
    tup["ID"]=crisis.attrib.values()[0]
    for i in crisis :
      tup[i.tag]+=i.text
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    print str(tuple(ret))
    query(c, "insert into PersonKinds values " + str(tuple(ret)) + ";")

# -------------
# WCDB2_export
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
# WCDB2_print
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

c=login()
WCDB2_setup(c)
tree = ET.parse(StringIO("<Bar><PersonKind id=\"1\"><Name>Cela</Name></PersonKind><Person id=\"12\"><Name><Suffix>Waza</Suffix></Name></Person><Organization hcwd=\"45\"><Location><Locality>Austin</Locality></Location><ContactInfo><PostalAddress><Locality>Marchew</Locality></PostalAddress></ContactInfo></Organization><Crisis bazyl=\"123\"><Kind va=\"12\"/></Crisis><Crisis bazyl=\"0\"><Name>Cela</Name><Location><Locality>Austin</Locality></Location><Location><Locality>Boston</Locality><Country>USA</Country></Location><ExternalResources><ImageURL>www</ImageURL><VideoURL>d</VideoURL><ImageURL>ccc</ImageURL></ExternalResources></Crisis></Bar>")) #importing the XML
root = tree.getroot()
WCDB2_import(c, root)
