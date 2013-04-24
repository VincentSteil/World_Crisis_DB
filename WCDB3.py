# -------------------
# WCDB3.py
# Group name: Is Yuchen Here Today?
# Lab 5 - LAST
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
  #uncomment and change to variables if you want to ask for database
  """
  in1 = raw_input('Host: ')
  in2 = raw_input('Username: ')
  in3 = raw_input('Password: ')
  in4 = raw_input('Database: ')
  """
  c = _mysql.connect(
          host = "z",
          user = "iwo",
          passwd = "Ez0CbTAuV~",
          db = "cs327e_iwo")
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
# WCDB3_setup
# -------------

def WCDB3_setup(c):
  """
  This function sets up the MySQL database that we will use
  c is a mysql connection
  """
                #makes sure tables are deleted if they existed before
  t = query(c, "drop table if exists Crisis;")
  assert t is None
  t = query(c, "drop table if exists Organization;")
  assert t is None
  t = query(c, "drop table if exists Person;")
  assert t is None
  t = query(c, "drop table if exists Location;")
  assert t is None
  t = query(c, "drop table if exists HumanImpact;")
  assert t is None
  t = query(c, "drop table if exists ResourceNeeded;")
  assert t is None
  t = query(c, "drop table if exists WaysToHelp;")
  assert t is None
  t = query(c, "drop table if exists ExternalResource;")
  assert t is None
  t = query(c, "drop table if exists CrisisOrganization;")
  assert t is None
  t = query(c, "drop table if exists OrganizationPerson;")
  assert t is None
  t = query(c, "drop table if exists PersonCrisis;")
  assert t is None
  t = query(c, "drop table if exists CrisisKind;")
  assert t is None
  t = query(c, "drop table if exists OrganizationKind;")
  assert t is None
  t = query(c, "drop table if exists PersonKind;")
  assert t is None
                #creates tables
  t = query(c, """    
    CREATE TABLE Crisis (
id char(100) NOT NULL
PRIMARY KEY,
name text NOT NULL,
kind char(100) NOT NULL
REFERENCES CrisisKind(id),
start_date date NOT NULL,
start_time time,
end_date date,
end_time time,
economic_impact char(100) NOT NULL
);
  """)

  t = query(c, """    
    CREATE TABLE Organization (
id char(100) NOT NULL
PRIMARY KEY,
name char(100) NOT NULL,
kind char(100) NOT NULL
REFERENCES OrganizationKind(id),
history text NOT NULL,
telephone char(100) NOT NULL,
fax char(100) NOT NULL,
email char(100) NOT NULL,
street_address char(100) NOT NULL,
locality char(100) NOT NULL,
region char(100) NOT NULL,
postal_code char(100) NOT NULL,
country char(100) NOT NULL
);
  """)

  t = query(c, """    
    CREATE TABLE Person (
id char(100) NOT NULL
PRIMARY KEY,
first_name char(100) NOT NULL,
middle_name char(100),
last_name char(100) NOT NULL,
suffix char(100),
kind char(100) NOT NULL
REFERENCES PersonKind(id)
);
  """)
  
  t = query(c, """    
    CREATE TABLE Location (
id int NOT NULL AUTO_INCREMENT
PRIMARY KEY,
entity_type ENUM('C', 'O', 'P') NOT NULL,
entity_id char(100) NOT NULL,
locality char(100),
region char(100),
country char(100)
);
  """)
  #print "Paszyn"

  t = query(c, """    
    CREATE TABlE HumanImpact (
id int NOT NULL AUTO_INCREMENT
PRIMARY KEY,
crisis_id char(100) NOT NULL
REFERENCES Crisis(id),
type char(100) NOT NULL,
number int NOT NULL
);
  """)
  t = query(c, """    
    CREATE TABLE ResourceNeeded (
id int NOT NULL AUTO_INCREMENT
PRIMARY KEY,
crisis_id char(100) NOT NULL
REFERENCES Crisis(id),
description text
);
  """)

  t = query(c, """    
    CREATE TABLE WaysToHelp (
id int NOT NULL AUTO_INCREMENT
PRIMARY KEY,
crisis_id char(100) NOT NULL
REFERENCES Crisis(id),
description text
);
  """)

  t = query(c, """    
    CREATE TABLE ExternalResource (
id int NOT NULL AUTO_INCREMENT
PRIMARY KEY,
entity_type ENUM('C', 'O', 'P') NOT NULL,
entity_id char(100) NOT NULL,
type ENUM('IMAGE', 'VIDEO', 'MAP', 'SOCIAL_NETWORK', 'CITATION', 'EXTERNAL_LINK') NOT NULL,
link text NOT NULL
);
  """)

  t = query(c, """    
    CREATE TABlE CrisisOrganization (
id_crisis char(100) NOT NULL
REFERENCES Crisis(id),
id_organization char(100) NOT NULL
REFERENCES Organization(id),
PRIMARY KEY (id_crisis, id_organization)
)
  """)

  t = query(c, """    
    CREATE TABLE OrganizationPerson (
id_organization char(100) NOT NULL
REFERENCES Organization(id),
id_person char(100) NOT NULL
REFERENCES Person(id),
PRIMARY KEY (id_organization, id_person)
);
  """)

  t = query(c, """    
    CREATE TABLE PersonCrisis (
id_person char(100) NOT NULL
REFERENCES Person(id),
id_crisis char(100) NOT NULL
REFERENCES Crisis(id),
PRIMARY KEY (id_person, id_crisis)
);
  """)

  t = query(c, """    
    CREATE TABLE CrisisKind (
id char(100) NOT NULL
PRIMARY KEY,
name char(100) NOT NULL,
description text NOT NULL
);
  """)

  t = query(c, """    
    CREATE TABLE OrganizationKind (
id char(100) NOT NULL
PRIMARY KEY,
name char(100) NOT NULL,
description text NOT NULL
);
  """)

  t = query(c, """    
    CREATE TABLE PersonKind (
id char(100) NOT NULL
PRIMARY KEY,
name char(100) NOT NULL,
description text NOT NULL
);
  """)

  assert t is None

# -------------
# WCDB3_import
# -------------

def WCDB3_import(c, root):
  """
  This function imports the XML instance to the MySQL database
  c is a mysql connection
  tree is an ElementTree
  """
  #This is how we do it: findalls and populating if the id does not exist or even without if if can get away with, bitch!
  #Crises
  for crisis in root.iter('Crisis'):
    tup = {"ID" : "", "Name" : "", "Kind" : "", "Location" : [], "StartDateTime" : [], "EndDateTime" : [],
           "HumanImpact" : [], "EconomicImpact" : "", "ResourceNeeded" : [], "WaysToHelp" : [], "ExternalResources" : [],
           "RelatedPersons" : [], "RelatedOrganizations" : []}
    ordering = ["ID", "Name", "Kind", "StartDateTime", "EndDateTime",
            "EconomicImpact"]
    orderingLoc = ["Locality", "Region", "Country"]
    transER = {"ImageURL" : "IMAGE", "VideoURL" : "VIDEO", "MapURL":"MAP", "SocialNetworkURL":"SOCIAL_NETWORK", "Citation":"CITATION", "ExternalLinkURL":"EXTERNAL_LINK"}
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
        tup[i.tag].append([i.find("Type").text, i.find("Number").text])
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


    ret = ["NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"]
    cttr=0;
    for h in ordering:
      if h=="StartDateTime" or h=="EndDateTime":
        tit=cttr+2
        for kk in tup[h]:
          ret[cttr]=kk
          cttr+=1
        cttr=tit
      else:
        ret[cttr]=(str(tup[h]))
        cttr+=1
    query(c, "delete from Crisis where id = \"" + ret[0] + "\";")
    query(c, "insert into Crisis values " + str(tuple(ret)).replace("\"NULL\"", "NULL") + ";")
    for l in tup["Location"]:
        retLoc=[]
        
        for h in orderingLoc:
            if h in l.keys():
                retLoc.append(l[h])
            else:
                retLoc.append("NULL");
        #print retLoc
        query(c, "delete from Location where (entity_type = 'C' and entity_id = \""+ret[0]+"\" and locality = \""+retLoc[0]+"\" and region = \""+retLoc[1]+"\" and country = \""+retLoc[2]+"\");")
        query(c, "insert into Location (entity_type, entity_id, locality, region, country) values ('C', \""+ret[0]+"\","+str(retLoc)[1:-1].replace("\"NULL\"", "NULL") +");")
    """ 
    <w><Crisis id="ss"><Location><Locality>dd</Locality></Location><HumanImpact><Type>kali</Type><Number>123</Number></HumanImpact><ResourceNeeded>cat</ResourceNeeded><ResourceNeeded>dog</ResourceNeeded>
     <ExternalResources><ImageURL>Bal</ImageURL><MapURL>Cyryl</MapURL></ExternalResources></Crisis>
     <Organization id="cela"><Name>Harpuny</Name><RelatedPersons><RelatedPerson vit="e"/></RelatedPersons></Organization>
     <Person id="e"><Name><FirstName>Jacenty</FirstName><Suffix>Baster</Suffix></Name></Person>
     <CrisisKind id="a"><Name>Habsburg</Name></CrisisKind>
     </w>
    """
    #print query(c, "select * from ExternalResource;")
    for l in tup["HumanImpact"]:
        query(c, "delete from HumanImpact where (crisis_id = \""+ret[0]+"\" and type = \""+l[0]+"\" and number = \""+l[1]+"\");")
        query(c, "insert into HumanImpact (crisis_id, type, number) values (\""+ret[0]+"\", \""+l[0]+"\", "+l[1]+");")
    for l in tup["ResourceNeeded"]:
        query(c, "delete from ResourceNeeded where (crisis_id = \""+ret[0]+"\" and description = \""+l+"\");")
        query(c, "insert into ResourceNeeded (crisis_id, description) values (\""+ret[0]+"\", \""+l+"\");")
    for l in tup["WaysToHelp"]:
        query(c, "delete from WaysToHelp where (crisis_id = \""+ret[0]+"\" and description = \""+l+"\");")
        query(c, "insert into WaysToHelp (crisis_id, description) values (\""+ret[0]+"\", \""+l+"\");")
    for l in tup["ExternalResources"]:
        query(c, "delete from ExternalResource where (entity_type= 'C' and entity_id = \""+ret[0]+"\" and type = \""+transER[l[0]]+"\" and link = \""+l[1]+"\");")
        query(c, "insert into ExternalResource (entity_type, entity_id, type, link) values ('C', \""+ret[0]+"\", '"+transER[l[0]]+"', \""+l[1]+"\");")
    for l in tup["RelatedOrganizations"]:
        query(c, "delete from CrisisOrganization where (id_crisis = \""+ret[0]+"\" and id_organization = \""+l+"\");")
        query(c, "insert into CrisisOrganization (id_crisis, id_organization) values (\""+ret[0]+"\", \""+l+"\");")
    for l in tup["RelatedPersons"]:
        query(c, "delete from PersonCrisis where (id_crisis = \""+ret[0]+"\" and id_person = \""+l+"\");")
        query(c, "insert into PersonCrisis (id_person, id_crisis) values (\""+l+"\", \""+ret[0]+"\");")
    #print query(c, "select * from ExternalResource;")
    #print "Caro"
   #Orgs
  for crisis in root.iter('Organization'):
    tup = {"ID" : "", "Name" : "", "Kind" : "", "Location" : [], "History" : "", "Telephone" : "",
           "Fax" : "", "Email" : "", "StreetAddress" : "", "Locality" : "", "Region" : "",
           "PostalCode" : "", "Country" : "", "ExternalResources" : [], "RelatedPersons" : [], "RelatedCrises" : []}
    ordering = ["ID", "Name", "Kind", "History", "Telephone",
           "Fax", "Email", "StreetAddress", "Locality", "Region",
           "PostalCode", "Country"]
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

    ret = ["NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"]
    cttr=0;
    for h in ordering:
        ret[cttr]=(str(tup[h]))
        cttr+=1;
    query(c, "delete from Organization where id = \"" + ret[0] + "\";")
    query(c, "insert into Organization values " + str(tuple(ret)).replace("\"NULL\"", "NULL") + ";")
    for l in tup["Location"]:
        retLoc=[]
        
        for h in orderingLoc:
            if h in l.keys():
                retLoc.append(l[h])
            else:
                retLoc.append("NULL");
        #print retLoc
        query(c, "delete from Location where (entity_type = 'O' and entity_id = \""+ret[0]+"\" and locality = \""+retLoc[0]+"\" and region = \""+retLoc[1]+"\" and country = \""+retLoc[2]+"\");")
        query(c, "insert into Location (entity_type, entity_id, locality, region, country) values ('O', \""+ret[0]+"\","+str(retLoc)[1:-1].replace("\"NULL\"", "NULL") +");")
    for l in tup["ExternalResources"]:
        query(c, "delete from ExternalResource where (entity_type= 'O' and entity_id = \""+ret[0]+"\" and type = \""+transER[l[0]]+"\" and link = \""+l[1]+"\");")
        query(c, "insert into ExternalResource (entity_type, entity_id, type, link) values ('O', \""+ret[0]+"\", '"+transER[l[0]]+"', \""+l[1]+"\");")
    for l in tup["RelatedPersons"]:
        query(c, "delete from OrganizationPerson where (id_person = \""+l+"\" and id_organization = \""+ret[0]+"\");")
        query(c, "insert into OrganizationPerson (id_organization, id_person) values (\""+ret[0]+"\", \""+l+"\");")
    #print query(c, "select * from OrganizationPerson;")
    #print "Halter"
    #persons
  for crisis in root.iter('Person'):
    tup = {"ID" : "", "FirstName" : "", "MiddleName" : "", "LastName" : "", "Suffix" : "", "Kind" : "", "Location" : [],
           "ExternalResources" : [], "RelatedCrises" : [], "RelatedOrganizations" : []}
    ordering = ["ID", "FirstName", "MiddleName", "LastName", "Suffix", "Kind"]
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

    ret = ["NULL", "NULL", "NULL", "NULL", "NULL", "NULL"]
    cttr=0;
    for h in ordering:
        if len(tup[h])>0:
            ret[cttr]=(str(tup[h]))
        cttr+=1;
    query(c, "delete from Person where id = \"" + ret[0] + "\";")
    query(c, "insert into Person values " + str(tuple(ret)).replace("\"NULL\"", "NULL") + ";")
    for l in tup["Location"]:
        retLoc=[]
        
        for h in orderingLoc:
            if h in l.keys():
                retLoc.append(l[h])
            else:
                retLoc.append("NULL");
        #print retLoc
        query(c, "delete from Location where (entity_type = 'P' and entity_id = \""+ret[0]+"\" and locality = \""+retLoc[0]+"\" and region = \""+retLoc[1]+"\" and country = \""+retLoc[2]+"\");")
        query(c, "insert into Location (entity_type, entity_id, locality, region, country) values ('P', \""+ret[0]+"\","+str(retLoc)[1:-1].replace("\"NULL\"", "NULL") +");")
    for l in tup["ExternalResources"]:
        query(c, "delete from ExternalResource where (entity_type= 'C' and entity_id = \""+ret[0]+"\" and type = \""+transER[l[0]]+"\" and link = \""+l[1]+"\");")
        query(c, "insert into ExternalResource (entity_type, entity_id, type, link) values ('P', \""+ret[0]+"\", '"+transER[l[0]]+"', \""+l[1]+"\");")
    #print query(c, "select * from Person;")
    #print "Pert"
  #Crisis kinds
  for crisis in root.iter('CrisisKind'):
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
    query(c, "delete from CrisisKind where id = \"" + ret[0] + "\";")
    query(c, "insert into CrisisKind values " + str(tuple(ret)) + ";")
    #print query(c, "select * from CrisisKind;")
    #print "Johannes"
  #organization kinds
  for crisis in root.iter('OrganizationKind'):
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
    query(c, "delete from OrganizationKind where id = \"" + ret[0] + "\";")
    query(c, "insert into OrganizationKind values " + str(tuple(ret)) + ";")
  #person kinds
  for crisis in root.iter('PersonKind'):
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
    query(c, "delete from PersonKind where id = \"" + ret[0] + "\";")
    query(c, "insert into PersonKind values " + str(tuple(ret)) + ";")

# -------------
# WCDB3_export
# -------------

def WCDB3_export(c):
  """
  This function exports the MySQL database to XML file
  c is a mysql connection
  """
  transER = {"IMAGE" :"ImageURL", "VIDEO":"VideoURL" , "MAP":"MapURL", "SOCIAL_NETWORK":"SocialNetworkURL", "CITATION":"Citation", "EXTERNAL_LINK":"ExternalLinkURL"}
  ret = ET.Element("WorldCrises")
      #exports crises
  t = query(c, "select * from Crisis;")
  for i in t :
    temp = ET.SubElement(ret, "Crisis", {"crisisIdent" : i[0]})
    n=ET.SubElement(temp, "Name")
    n.text=i[1]
    n=ET.SubElement(temp, "Kind", {"crisisKindIdent" : i[2]})
    for j in query(c, "select * from Location where entity_type = 'C' and entity_id = \""+i[0]+"\";"):
      m=ET.SubElement(temp, "Location")
      order = ["Locality", "Region", "Country"]
      for k in range(0, 3):
        if j[k+3] != "NULL" and len(j[k+3])>0:
          n=ET.SubElement(m, order[k])
          n.text=j[k+3]
    m=ET.SubElement(temp, "StartDateTime")
    n=ET.SubElement(m, "Date")
    if i[3]!="NULL" and len(i[3])>0:
      n.text=i[3]
    if i[4]!="NULL" and len(i[4])>0:
      n=ET.SubElement(m, "Time")
      n.text=i[4]
    if i[5]!="NULL" and len(i[5])>0:
      m=ET.SubElement(temp, "EndDateTime")
      n=ET.SubElement(m, "Date")
      n.text=i[5]
      if i[6]!="NULL" and len(i[6])>0:
        n=ET.SubElement(m, "Time")
        n.text=i[6]

    for j in query(c, "select * from HumanImpact where crisis_id = \""+i[0]+"\";"):
      m=ET.SubElement(temp, "HumanImpact")
      n=ET.SubElement(m, "Type")
      n.text=j[2]
      n=ET.SubElement(m, "Number")
      n.text=j[3]
    n=ET.SubElement(temp, "EconomicImpact")
    n.text=i[7]
    for j in query(c, "select * from ResourceNeeded where crisis_id = \""+i[0]+"\";"):
      n=ET.SubElement(temp, "ResourceNeeded")
      n.text=j[2]
    for j in query(c, "select * from WaysToHelp where crisis_id = \""+i[0]+"\";"):
      n=ET.SubElement(temp, "WaysToHelp")
      n.text=j[2]
    m=ET.SubElement(temp, "ExternalResources")
    for j in query(c, "select * from ExternalResource where entity_type = 'C' and entity_id = \""+i[0]+"\";"):
      n=ET.SubElement(m, transER[j[3]])
      n.text=j[4]
    if len(query(c, "select * from PersonCrisis where id_crisis = \""+i[0]+"\";"))>0:
        m=ET.SubElement(temp, "RelatedPersons")
    for j in query(c, "select * from PersonCrisis where id_crisis = \""+i[0]+"\";"):
         n=ET.SubElement(m, "RelatedPerson", {"personIdent":j[0]})

    if len(query(c, "select * from CrisisOrganization where id_crisis = \""+i[0]+"\";"))>0:
        m=ET.SubElement(temp, "RelatedOrganizations")
    for j in query(c, "select * from CrisisOrganization where id_crisis = \""+i[0]+"\";"):
         n=ET.SubElement(m, "RelatedOrganization", {"organizationIdent":j[1]})

        #exports organizations
  t = query(c, "select * from Organization;")
  for i in t :
    temp = ET.SubElement(ret, "Organization", {"organizationIdent" : i[0]})
    n=ET.SubElement(temp, "Name")
    n.text=i[1]
    n=ET.SubElement(temp, "Kind", {"organizationKindIdent" : i[2]})
    for j in query(c, "select * from Location where entity_type = 'O' and entity_id = \""+i[0]+"\";"):
      m=ET.SubElement(temp, "Location")
      order = ["Locality", "Region", "Country"]
      for k in range(0, 3):
        if j[k+3] != "NULL" and len(j[k+3])>0:
          n=ET.SubElement(m, order[k])
          n.text=j[k+3]
    n=ET.SubElement(temp, "History")
    n.text=i[3]
    m=ET.SubElement(temp, "ContactInfo")
    n=ET.SubElement(m, "Telephone")
    n.text=i[4]
    n=ET.SubElement(m, "Fax")
    n.text=i[5]
    n=ET.SubElement(m, "Email")
    n.text=i[6]
    n=ET.SubElement(m, "PostalAddress")
    o=ET.SubElement(n, "StreetAddress")
    o.text=i[7]
    o=ET.SubElement(n, "Locality")
    o.text=i[8]
    o=ET.SubElement(n, "Region")
    o.text=i[9]
    o=ET.SubElement(n, "PostalCode")
    o.text=i[10]
    o=ET.SubElement(n, "Country")
    o.text=i[11]
    m=ET.SubElement(temp, "ExternalResources")
    for j in query(c, "select * from ExternalResource where entity_type = 'O' and entity_id = \""+i[0]+"\";"):
      n=ET.SubElement(m, transER[j[3]])
      n.text=j[4]

    if len(query(c, "select * from CrisisOrganization where id_organization = \""+i[0]+"\";"))>0:
        m=ET.SubElement(temp, "RelatedOrganizations")
    for j in query(c, "select * from CrisisOrganization where id_organization = \""+i[0]+"\";"):
         n=ET.SubElement(m, "RelatedOrganization", {"crisisIdent":j[0]})

    if len(query(c, "select * from OrganizationPerson where id_organization = \""+i[0]+"\";"))>0:
        m=ET.SubElement(temp, "RelatedPersons")
    for j in query(c, "select * from OrganizationPerson where id_organization = \""+i[0]+"\";"):
         n=ET.SubElement(m, "RelatedPerson", {"personIdent":j[1]})

        #exports persons
  t = query(c, "select * from Person;")
  for i in t :
    temp = ET.SubElement(ret, "Person", {"personIdent" : i[0]})
    m=ET.SubElement(temp, "Name")
    n=ET.SubElement(m, "FirstName")
    n.text=i[1]
    if i[2]!="NULL" and len(i[2])>0:
      n=ET.SubElement(m, "MiddleName")
      n.text=i[2]
    n=ET.SubElement(m, "LastName")
    n.text=i[3]
    if i[4]!="NULL" and len(i[4])>0:
      n=ET.SubElement(m, "Suffix")
      n.text=i[4]
    n=ET.SubElement(temp, "Kind", {"personKindIdent" : i[5]})
    for j in query(c, "select * from Location where entity_type = 'P' and entity_id = \""+i[0]+"\";"):
      m=ET.SubElement(temp, "Location")
      order = ["Locality", "Region", "Country"]
      for k in range(0, 3):
        if j[k+3] != "NULL" and len(j[k+3])>0:
          n=ET.SubElement(m, order[k])
          n.text=j[k+3]
    m=ET.SubElement(temp, "ExternalResources")
    for j in query(c, "select * from ExternalResource where entity_type = 'P' and entity_id = \""+i[0]+"\";"):
      n=ET.SubElement(m, transER[j[3]])
      n.text=j[4]

    if len(query(c, "select * from PersonCrisis where id_person = \""+i[0]+"\";"))>0:
        m=ET.SubElement(temp, "RelatedPersons")
    for j in query(c, "select * from PersonCrisis where id_person = \""+i[0]+"\";"):
         n=ET.SubElement(m, "RelatedPerson", {"crisisIdent":j[1]})

    if len(query(c, "select * from OrganizationPerson where id_organization = \""+i[0]+"\";"))>0:
        m=ET.SubElement(temp, "RelatedPersons")
    for j in query(c, "select * from OrganizationPerson where id_organization = \""+i[0]+"\";"):
         n=ET.SubElement(m, "RelatedPerson", {"organizationIdent":j[0]})

        #exports CrisisKinds
  t = query(c, "select * from CrisisKind;")
  for i in t :
    temp = ET.SubElement(ret, "CrisisKind", {"crisisKindIdent" : i[0]})
    n=ET.SubElement(temp, "Name")
    n.text=i[1]
    n=ET.SubElement(temp, "Description")
    n.text=i[2]
        #exports OrgKinds
  t = query(c, "select * from OrganizationKind;")
  for i in t :
    temp = ET.SubElement(ret, "OrganizationKind", {"organizationKindIdent" : i[0]})
    n=ET.SubElement(temp, "Name")
    n.text=i[1]
    n=ET.SubElement(temp, "Description")
    n.text=i[2]
        #exports PersonKinds
  t = query(c, "select * from PersonKind;")
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
# WCDB3_print
# -------------

def WCDB3_print(w, tree):
  """
  This function prints tree to writer w
  w is a writer
  tree is a string to print
  """

  x = xml.dom.minidom.parseString(tree)
  woop = x.toprettyxml()
  w.write(woop) #printing to the console

# -------------
# WCDB3_run
# -------------

  
def WCDB3_run(r ,w):
  """
  This function reads an XML from the input then imports it to MySQL then exports it from MySQL and prints the XML
  r is a reader
  w is a writer
  """
  c=login()
  WCDB3_setup(c)
  strr = """ 
    <w><Crisis id="ss"><Location><Locality>dd</Locality><Country>USA</Country></Location><HumanImpact><Type>kali</Type><Number>123</Number></HumanImpact><ResourceNeeded>cat</ResourceNeeded><ResourceNeeded>dog</ResourceNeeded>
     <ExternalResources><ImageURL>Bal</ImageURL><MapURL>Cyryl</MapURL></ExternalResources></Crisis>
     <Crisis id="bel"></Crisis>
     <Organization id="cela"><Name>Harpuny</Name><ContactInfo><Telephone>0800100100</Telephone><PostalAddress></PostalAddress></ContactInfo><RelatedPersons><RelatedPerson vit="e"/></RelatedPersons></Organization>
     <Person id="e"><Name><FirstName>Jacenty</FirstName><Suffix>Baster</Suffix></Name></Person>
     <CrisisKind id="a"><Name>Habsburg</Name></CrisisKind>
     </w>
    """
  strr=r.read()
  assert len(strr)>0
  strr = strr.replace("&", "&amp;")
  strr = "<qq>"+strr+"</qq>"
  tree = ET.parse(StringIO(strr)) #importing the XML
  root = tree.getroot()
  WCDB3_import(c, root)
  xx=WCDB3_export(c)
  WCDB3_print(w, ET.tostring(xx)) #sending tree to the printer

   