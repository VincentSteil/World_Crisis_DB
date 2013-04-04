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
import ast
import xml.dom.minidom

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
                #makes sure tables are deleted if they existed before
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
                #creates tables
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
  This function imports the XML instance to the MySQL database
  c is a mysql connection
  tree is an ElementTree
  """
  #Crises
  for crisis in root.findall('Crisis'):
    tup = {"ID" : "", "Name" : "", "Kind" : "", "Location" : [], "StartDateTime" : [], "EndDateTime" : [],
           "HumanImpact" : [], "EconomicImpact" : "", "ResourceNeeded" : [], "WaysToHelp" : [], "ExternalResources" : [],
           "RelatedPersons" : [], "RelatedOrganizations" : []}
    ordering = ["ID", "Name", "Kind", "Location", "StartDateTime", "EndDateTime",
           "HumanImpact", "EconomicImpact", "ResourceNeeded", "WaysToHelp", "ExternalResources",
           "RelatedPersons", "RelatedOrganizations"]
    tup["ID"]=crisis.attrib.values()[0]
    
    for i in crisis :
      if i.tag=="Kind":
        tup["Kind"]=i.attrib.values()[0]
      elif len(i) == 0 :
        if i.text != None and i.tag in tup.keys():
          if type(tup[i.tag])==list:
            tup[i.tag]+=[i.text]
          else:
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
          tup[i.tag]=[i.find("Date").text]
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
            tup[i.tag]+=[j.attrib.values()[0]]
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    query(c, "insert into Crises values " + str(tuple(ret)) + ";")
  
   #Orgs
  for crisis in root.findall('Organization'):
    tup = {"ID" : "", "Name" : "", "Kind" : "", "Location" : [], "History" : "", "Telephone" : "",
           "Fax" : "", "Email" : "", "StreetAddress" : "", "Locality" : "", "Region" : "",
           "PostalCode" : "", "Country" : "", "ExternalResources" : [], "RelatedPersons" : [], "RelatedCrises" : []}
    ordering = ["ID", "Name", "Kind", "Location", "History", "Telephone",
           "Fax", "Email", "StreetAddress", "Locality", "Region",
           "PostalCode", "Country", "ExternalResources", "RelatedPersons", "RelatedCrises"]
    tup["ID"]=crisis.attrib.values()[0]
    
    for i in crisis :
      if i.tag=="Kind":
        tup["Kind"]=i.attrib.values()[0]
      elif len(i) == 0 :
        if i.text != None and i.tag in tup.keys():
          if type(tup[i.tag])==list:
            tup[i.tag]+=[i.text]
          else:
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
            tup[i.tag]+=[j.attrib.values()[0]]
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    query(c, "insert into Organizations values " + str(tuple(ret)) + ";")  
    #persons
  for crisis in root.findall('Person'):
    tup = {"ID" : "", "FirstName" : "", "MiddleName" : "", "LastName" : "", "Suffix" : "", "Kind" : "", "Location" : [],
           "ExternalResources" : [], "RelatedCrises" : [], "RelatedOrganizations" : []}
    ordering = ["ID", "FirstName", "MiddleName", "LastName", "Suffix", "Kind", "Location", "ExternalResources",
           "RelatedCrises", "RelatedOrganizations"]
    tup["ID"]=crisis.attrib.values()[0]
    
    for i in crisis :
      if i.tag=="Kind":
        tup["Kind"]=i.attrib.values()[0]
      elif len(i) == 0 :
        if i.text != None and i.tag in tup.keys():
          if type(tup[i.tag])==list:
            tup[i.tag]+=[i.text]
          else:
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
            tup[i.tag]+=[j.attrib.values()[0]]
    
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    query(c, "insert into Persons values " + str(tuple(ret)) + ";")
  #Crisis kinds
  for crisis in root.findall('CrisisKind'):
    tup = {"ID" : "", "Name" : "", "Description" : ""}
    ordering = ["ID", "Name", "Description"]
    tup["ID"]=crisis.attrib.values()[0]
    for i in crisis :
      if i.text == None:
        i.text=""
      tup[i.tag]+=i.text
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    query(c, "insert into CrisisKinds values " + str(tuple(ret)) + ";")
  #organization kinds
  for crisis in root.findall('OrganizationKind'):
    tup = {"ID" : "", "Name" : "", "Description" : ""}
    ordering = ["ID", "Name", "Description"]
    tup["ID"]=crisis.attrib.values()[0]
    for i in crisis :
      if i.text == None:
        i.text=""
      tup[i.tag]+=i.text
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    query(c, "insert into OrgKinds values " + str(tuple(ret)) + ";")
  #person kinds
  for crisis in root.findall('PersonKind'):
    tup = {"ID" : "", "Name" : "", "Description" : ""}
    ordering = ["ID", "Name", "Description"]
    tup["ID"]=crisis.attrib.values()[0]
    for i in crisis :
      if i.text == None:
        i.text=""
      tup[i.tag]+=i.text
    ret = list()
    for h in ordering:
      ret.append(str(tup[h]))
    query(c, "insert into PersonKinds values " + str(tuple(ret)) + ";")

# -------------
# WCDB2_export
# -------------

def WCDB2_export(c):
  """
  This function exports the MySQL database to XML file
  c is a mysql connection
  """
  ret = ET.Element("WorldCrises")
      #exports crises
  t = query(c, "select * from Crises;")
  for i in t :
    temp = ET.SubElement(ret, "Crisis", {"crisisIdent" : i[0]})
    n=ET.SubElement(temp, "Name")
    n.text=i[1]
    n=ET.SubElement(temp, "Kind", {"crisisKindIdent" : i[2]})
    for j in ast.literal_eval(i[3]):
      m=ET.SubElement(temp, "Location")
      order = ["Locality", "Region", "Country"]
      for k in order:
        if k in j:
          n=ET.SubElement(m, k)
          n.text=j[k]
    m=ET.SubElement(temp, "StartDateTime")
    ii=ast.literal_eval(i[4])
    n=ET.SubElement(m, "Date")
    if len(ii)>0:
      n.text=ii[0]
    if len(ii)==2:
      n=ET.SubElement(m, "Time")
      n.text=ii[1]
    
    ii=ast.literal_eval(i[5])
    if len(ii)>0 :
      m=ET.SubElement(temp, "EndDateTime")
      n=ET.SubElement(m, "Date")
      n.text=ii[0]
      if len(ii)==2:
        n=ET.SubElement(m, "Time")
        n.text=ii[1]

    ii=ast.literal_eval(i[6])
    if len(ii)>0 :
      m=ET.SubElement(temp, "HumanImpact")
      n=ET.SubElement(m, "Type")
      n.text=ii[0]
      n=ET.SubElement(m, "Number")
      n.text=ii[1]
    n=ET.SubElement(temp, "EconomicImpact")
    n.text=i[7]
    ii=ast.literal_eval(i[8])
    for j in ii:
      n=ET.SubElement(temp, "ResourceNeeded")
      n.text=j
    ii=ast.literal_eval(i[9])
    for j in ii:
      n=ET.SubElement(temp, "WaysToHelp")
      n.text=j
    m=ET.SubElement(temp, "ExternalResources")
    ii=ast.literal_eval(i[10])
    for j in ii:
      n=ET.SubElement(m, j[0])
      n.text=j[1]

    ii=ast.literal_eval(i[11])
    if len(ii)>0:
      m=ET.SubElement(temp, "RelatedPersons")
      for j in ii:
         n=ET.SubElement(m, "RelatedPerson", {"personIdent":j})
        
    ii=ast.literal_eval(i[12])
    if len(ii)>0:
      m=ET.SubElement(temp, "RelatedOrganizations")
      for j in ii:
         n=ET.SubElement(m, "RelatedOrganization", {"organizationIdent":j})
        #exports organizations
  t = query(c, "select * from Organizations;")
  for i in t :
    temp = ET.SubElement(ret, "Organization", {"organizationIdent" : i[0]})
    n=ET.SubElement(temp, "Name")
    n.text=i[1]
    n=ET.SubElement(temp, "Kind", {"organizationKindIdent" : i[2]})
    for j in ast.literal_eval(i[3]):
      m=ET.SubElement(temp, "Location")
      order = ["Locality", "Region", "Country"]
      for k in order:
        if k in j:
          n=ET.SubElement(m, k)
          n.text=j[k]
    n=ET.SubElement(temp, "History")
    n.text=i[4]
    m=ET.SubElement(temp, "ContactInfo")
    n=ET.SubElement(m, "Telephone")
    n.text=i[5]
    n=ET.SubElement(m, "Fax")
    n.text=i[6]
    n=ET.SubElement(m, "Email")
    n.text=i[7]
    n=ET.SubElement(m, "PostalAddress")
    o=ET.SubElement(n, "StreetAddress")
    o.text=i[8]
    o=ET.SubElement(n, "Locality")
    o.text=i[9]
    o=ET.SubElement(n, "Region")
    o.text=i[10]
    o=ET.SubElement(n, "PostalCode")
    o.text=i[11]
    o=ET.SubElement(n, "Country")
    o.text=i[12]
    m=ET.SubElement(temp, "ExternalResources")
    ii=ast.literal_eval(i[13])
    for j in ii:
      n=ET.SubElement(m, j[0])
      n.text=j[1]
    ii=ast.literal_eval(i[14])
    if len(ii)>0:
      m=ET.SubElement(temp, "RelatedCrises")
      for j in ii:
         n=ET.SubElement(m, "RelatedCrisis", {"crisisIdent":j})
        
    ii=ast.literal_eval(i[15])
    if len(ii)>0:
      m=ET.SubElement(temp, "RelatedPersons")
      for j in ii:
         n=ET.SubElement(m, "RelatedPerson", {"personIdent":j})
        #exports persons
  t = query(c, "select * from Persons;")
  for i in t :
    temp = ET.SubElement(ret, "Person", {"personIdent" : i[0]})
    m=ET.SubElement(temp, "Name")
    n=ET.SubElement(m, "FirstName")
    n.text=i[1]
    if len(i[2])>0:
      n=ET.SubElement(m, "MiddleName")
      n.text=i[2]
    n=ET.SubElement(m, "LastName")
    n.text=i[3]
    if len(i[4])>0:
      n=ET.SubElement(m, "Suffix")
      n.text=i[4]
    n=ET.SubElement(temp, "Kind", {"personKindIdent" : i[5]})
    for j in ast.literal_eval(i[6]):
      m=ET.SubElement(temp, "Location")
      order = ["Locality", "Region", "Country"]
      for k in order:
        if k in j:
          n=ET.SubElement(m, k)
          n.text=j[k]
    m=ET.SubElement(temp, "ExternalResources")
    ii=ast.literal_eval(i[7])
    for j in ii:
      n=ET.SubElement(m, j[0])
      n.text=j[1]
    ii=ast.literal_eval(i[8])
    if len(ii)>0:
      m=ET.SubElement(temp, "RelatedCrises")
      for j in ii:
         n=ET.SubElement(m, "RelatedCrisis", {"crisisIdent":j})
    ii=ast.literal_eval(i[9])
    if len(ii)>0:
      m=ET.SubElement(temp, "RelatedOrganizations")
      for j in ii:
         n=ET.SubElement(m, "RelatedOrganization", {"organizationIdent":j})
        #exports CrisisKinds
  t = query(c, "select * from CrisisKinds;")
  for i in t :
    temp = ET.SubElement(ret, "CrisisKind", {"crisisKindIdent" : i[0]})
    n=ET.SubElement(temp, "Name")
    n.text=i[1]
    n=ET.SubElement(temp, "Description")
    n.text=i[2]
        #exports OrgKinds
  t = query(c, "select * from OrgKinds;")
  for i in t :
    temp = ET.SubElement(ret, "OrganizationKind", {"organizationKindIdent" : i[0]})
    n=ET.SubElement(temp, "Name")
    n.text=i[1]
    n=ET.SubElement(temp, "Description")
    n.text=i[2]
        #exports PersonKinds
  t = query(c, "select * from PersonKinds;")
  for i in t :
    temp = ET.SubElement(ret, "PersonKind", {"personKindIdent" : i[0]})
    n=ET.SubElement(temp, "Name")
    n.text=i[1]
    n=ET.SubElement(temp, "Description")
    n.text=i[2]
  assert t is not None
  assert ret is not None
  return ret
  

# -------------
# WCDB2_print
# -------------

def WCDB2_print(w, tree):
  """
  This function prints tree to writer w
  w is a writer
  tree is a string to print
  """

  x = xml.dom.minidom.parseString(tree)
  woop = x.toprettyxml()
  w.write(woop) #printing to the console

# -------------
# WCDB2_run
# -------------

  
def WCDB2_run(r ,w):
  """
  This function reads an XML from the input then imports it to MySQL then exports it from MySQL and prints the XML
  r is a reader
  w is a writer
  """
  c=login()
  WCDB2_setup(c)
  strr = r.read()
  assert len(strr)>0
  strr = strr.replace("&", "&amp;")
  tree = ET.parse(StringIO(strr)) #importing the XML
  root = tree.getroot()
  WCDB2_import(c, root)
  xx=WCDB2_export(c)
  WCDB2_print(w, ET.tostring(xx)) #sending tree to the printer
