use cs327e_iwo;

/*
1.  Which people are associated with more than one crisis?
*/

create temporary table Person_Crisis_Count as
	select distinct id_person, count(*) as count
	from PersonCrisis
	group by id_person;

select distinct id_person
from Person_Crisis_Count
where count > 1;

/*
2. For the past 5 decades, which countries had the most world crises per decade?
*/

create temporary table TwoThousands_Crises as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '2000-01-01' and Crisis.start_date < '2010-01-01'
	group by country;

create temporary table TwoThousands_Crises2 as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '2000-01-01' and Crisis.start_date < '2010-01-01'
	group by country;

create temporary table Ninetees_Crises as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '1990-01-01' and Crisis.start_date < '2000-01-01'
	group by country;

create temporary table Ninetees_Crises2 as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '1990-01-01' and Crisis.start_date < '2000-01-01'
	group by country;

create temporary table Eighties_Crises as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '1980-01-01' and Crisis.start_date < '1990-01-01'
	group by country;

create temporary table Eighties_Crises2 as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '1980-01-01' and Crisis.start_date < '1990-01-01'
	group by country;
	
create temporary table Seventies_Crises as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '1970-01-01' and Crisis.start_date < '1980-01-01'
	group by country;

create temporary table Seventies_Crises2 as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '1970-01-01' and Crisis.start_date < '1980-01-01'
	group by country;

create temporary table Sixties_Crises as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '1960-01-01' and Crisis.start_date < '1970-01-01'
	group by country;

create temporary table Sixties_Crises2 as
	select count(*) as count, Location.country as country
	from Crisis inner join Location
	on Crisis.id = Location.entity_id
	where Crisis.start_date >= '1960-01-01' and Crisis.start_date < '1970-01-01'
	group by country;

select country, '2000-2010' as decade
from TwoThousands_Crises
where not exists (
	select *
	from TwoThousands_Crises2
	where TwoThousands_Crises.count < TwoThousands_Crises2.count
	)
	
union

select country, '1990-2000' as decade
from Ninetees_Crises
where not exists (
	select *
	from Ninetees_Crises2
	where Ninetees_Crises.count < Ninetees_Crises2.count
	)

union

select country, '1980-1990' as decade
from Eighties_Crises
where not exists (
	select *
	from Eighties_Crises2
	where Eighties_Crises.count < Eighties_Crises2.count
	)
	
union

select country, '1970-1980' as decade
from Seventies_Crises
where not exists (
	select *
	from Seventies_Crises2
	where Seventies_Crises.count < Seventies_Crises2.count
	)
	
union

select country, '1960-1970' as decade
from Sixties_Crises
where not exists (
	select *
	from Sixties_Crises2
	where Sixties_Crises.count < Sixties_Crises2.count
	);




/*
3. What is the average death toll of accident crises?
*/

select avg(number)
from HumanImpact
where crisis_id in (
	select id
	from Crisis
	where kind = 'ACC' and type = 'Death'
	);
	
/*
4.  What is the average death toll of world crises per country?
*/

create temporary table T1 as
	select country, number
	from Location cross join HumanImpact
	where Location.entity_type = 'C' and Location.entity_id = HumanImpact.crisis_id;

select country, avg(number)
from T1
group by country;

/*
5. What is the most common resource needed?
*/

create temporary table Resource_Count as
	select description, count(*) as count
	from ResourceNeeded
	group by description;
	
create temporary table Resource_Count2 as
	select description, count(*) as count
	from ResourceNeeded
	group by description;
	
select description, count
from Resource_Count
where not exists (
	select *
	from Resource_Count2
	where Resource_Count.count < Resource_Count2.count
	);

/*
6. How many persons are related to crises located in countries other than their own?
*/

create temporary table Crisis_Country as
	select entity_id as id_crisis, country as ccountry
	from Location
	where entity_type = 'C';
	
create temporary table Person_Country as
	select entity_id as id_person, country as pcountry
	from Location
	where entity_type = 'P';
	
select count(distinct PersonCrisis.id_person)
from  Crisis_Country natural join Person_Country natural join PersonCrisis
where 	ccountry != pcountry;
		
/*
7. How many crises occurred during the 1960s?
*/

select count(id)
from Crisis
where start_date > '1960-01-01' and start_date < '1970-01-01';

/*
8. Which orgs are located outside the United States and were involved in more than 1 crisis?
*/

create temporary table Orgs_Country as
	select entity_id, country
	from Location
	where entity_type = 'O';
	
create temporary table Orgs_not_US as
	select id_organization, id_crisis
	from Orgs_Country, CrisisOrganization
	where Orgs_Country.entity_id = CrisisOrganization.id_organization and
 	  Orgs_Country.country != 'US' and
 	  Orgs_Country.country != 'United States' and
 	  Orgs_Country.country != 'USA' and
 	  Orgs_Country.country != 'United States of America';

create temporary table Orgs_not_US_crises_count as
	select id_organization, count(*) as count
	from Orgs_not_US
	group by id_organization;
	
	
select distinct id_organization
from Orgs_not_US_crises_count
where count > 1;

/*
9. Which Orgs, Crises, and Persons have the same location?
*/

select distinct entity_id, locality, region, country
from Location
order by locality, region, country;


/*
10. Which crisis has the minumum Human Impact? 
*/
select distinct crisis_id 
from HumanImpact as A
where not exists (
	select *
	from HumanImpact as B
	where A.number > B.number
	);

/*
11. Count the number of crises that each organization helped
Ez0CbTAuV~
*/

select distinct id_organization, count(*)
from CrisisOrganization
group by id_organization;
	
/*
12. Name and Postal Address of all orgs in California
*/

select name, street_address, locality, region, postal_code, country
from Organization
where region = 'California';

/*
13. List all crises that happened in the same state/region
*/

select entity_id, region
from Location
where (entity_type = 'C' and region not null)
order by region;

/*
14. Find the total number of human casualties caused by crises in the 1990s
*/

select sum(number)
from HumanImpact
where crisis_id in (
	select id
	from Crisis
	where start_date >= '1990-01-01' and start_date < '2000-01-01'
	);
	
/*
15. Find the organization(s) that has provided support on the most Crises 
*/	

create temporary table Organization_Crisis_Count as
	select distinct id_organization, count(*) as count
	from CrisisOrganization
	group by id_organization;
	
create temporary table Organization_Crisis_Count2 as
	select distinct id_organization, count(*) as count
	from CrisisOrganization
	group by id_organization;

select id_organization
from Organization_Crisis_Count as O1
where not exists (
	select *
	from Organization_Crisis_Count2 as O2
	where O1.count < O2.count
	);

/*
16. How many orgs are government based? 
*/

select count(*)
from Organization
where kind = 'AD' or kind = 'CB' or kind = 'GMB' or kind = 'GOV' or kind = 'IA' or kind = 'MO' or kind = 'NG' or kind = 'NS' or kind = 'GO';

/*
17. What is the total number of casualties across the DB?
*/

select sum(number)
from HumanImpact;

/*
18. What is the most common type/kind of crisis occuring in the DB?
*/

create temporary table Crisis_Kind_Count as
	select distinct kind, count(*) as count
	from Crisis
	group by kind;

create temporary table Crisis_Kind_Count2 as
	select distinct kind, count(*) as count
	from Crisis
	group by kind;

select kind
from Crisis_Kind_Count
where not exists (
	select *
	from Crisis_Kind_Count2
	where Crisis_Kind_Count.count < Crisis_Kind_Count2.count
	);

/*
19. Create a list of telephone numbers, emails, and other contact info for all orgs 
*/

select name, telephone, fax, email, street_address, locality, region, postal_code, country
from Organization;

/*
20. What is the longest-lating crisis? (if no end date, then ignore) 
*/

create temporary table Crisis_length as
	select id, datediff(end_date, start_date) as duration
	from Crisis
	where end_date is not null;

create temporary table Crisis_length2 as
	select id, datediff(end_date, start_date) as duration
	from Crisis
	where end_date is not null;

select id, duration
from Crisis_length
where not exists (
	select *
	from Crisis_length2
	where Crisis_length.duration < Crisis_length2.duration
	)
	and duration is not null;


/*
21. Which person(s) is involved or associated with the most organizations?
*/

create temporary table Person_organization_count as
	select id_person, count(*) as count
	from OrganizationPerson
	group by id_person;

create temporary table Person_organization_count2 as
	select id_person, count(*) as count
	from OrganizationPerson
	group by id_person;

select id_person
from Person_organization_count
where not exists (
	select *
	from Person_organization_count2
	where Person_organization_count.count < Person_organization_count2.count
	);

/*
22. How many hurricane crises (CrisisKind=HU)?
*/

select count(*)
from Crisis
where kind = 'HU';

/*
23. Name all humanitarian orgs in the DB
*/

select name
from Organization
where kind = 'HO';

/*
24. List the crises in the order when they occurred (earliest to latest)
*/

select id
from Crisis
order by start_date;



/*
25. Get the name and kind of all persons in the US (United States, USA, United States of America)
*/

select first_name, middle_name, last_name, kind
from Person
where id in (
	select entity_id
	from Location
	where country = 'USA' or country = 'US' or country = 'United States' or country = 'United States of America' and entity_type = 'P'	
	);


/*
26. Who has the longest name?
*/

create temporary table name_lengths as
	select id, (char_length(first_name) + char_length(middle_name) + char_length(last_name)) as length
	from Person;

create temporary table name_lengths2 as
	select id, (char_length(first_name) + char_length(middle_name) + char_length(last_name)) as length
	from Person;

select id
from name_lengths
where not exists (
	select *
	from name_lengths2
	where name_lengths.length < name_lengths2.length
	);

/*
27. Which kinds of crisis only have one crisis example?
*/

create temporary table Crisis_kind_count_single as
	select kind, count(*) as count
	from Crisis
	group by kind;
	
select kind
from Crisis_kind_count_single
where count = 1;

/*
28. Which people don't have a middle name?
*/ 

select id
from Person
where middle_name = 'NULL';

/*
29. What are the names that start with 'B'?
*/

select first_name, middle_name, last_name
from Person
where ASCII(first_name) = 66;

/*
30. List all the people associated with each country.
*/

select entity_id, country
from Location
where entity_type = 'P'
order by country;

/*
31. What crisis affected the most countries? 
*/

create temporary table Crisis_Location_count as 
	select entity_id, count(distinct country) as count
	from Location
	where entity_type = 'C'
	group by entity_id;

create temporary table Crisis_Location_count2 as 
	select entity_id, count(distinct country) as count
	from Location
	where entity_type = 'C'
	group by entity_id;

select entity_id
from Crisis_Location_count
where not exists (
	select *
	from Crisis_Location_count2
	where Crisis_Location_count.count < Crisis_Location_count2.count
	);
	
/*
32. What is the first (earliest) crisis in the first database?
*/

select id
from Crisis as C11
where not exists (
	select *
	from Crisis as C12
	where C11.start_date > C12.start_date
	);
	
/*
33. What is the number of organizations in the US?
*/

select count(country)
from Organization
where (country="United States" or country = "United States of America" or country = "US" or country = "USA");

/*
34. How many people are singers? 
*/

select count(kind)
from Person
where (kind = 'SNG');

/*
35. What is the number of leaders (current and former)? (PersonKind is "LD")
*/

select count(kind)
from Person
where kind = 'LD';

/*
36. Find the start date of every hurricane that occurred in the US
*/
	
select id, start_date
from Crisis
where id in (
	select entity_id
	from Location
	where country = 'USA' or country = 'US' or country = 'United States' or country = 'United States of America' and entity_type = 'C'	
	)
	and kind = 'HU';


/*
37. Number of natural disasters occurring from June 5th 2000 to June 5th 2012
*/

select count(*)
from Crisis
where 	start_date <= '2012-06-05' and start_date >= '2000-06-05' and
	(kind = 'EQ' or kind = 'FR' or kind = 'FL' or kind = 'HU' or kind = 'ME' or kind = 'ST' or kind = 'TO' or kind = 'TS' or kind = 'VO');


/*
38. Number of political figures grouped by country.
*/

select distinct country, count(*)
from Location
where entity_id in (
	select id
	from Person
	where kind = 'DI' or kind = 'FRC' or kind = 'GO' or kind = 'GOV' or kind = 'LD' or kind = 'PO' or kind = 'PR' or kind = 'PM' or kind = 'SA' or kind = 'AMB' or kind = 'VP'
	)
group by country;

/*
39. Location with the most number of natural disasters
*/

select locality, region, country, count(*)
from Location
where entity_id in (
	select id
	from Crisis
	where kind = 'EQ' or kind = 'FR' or kind = 'FL' or kind = 'HU' or kind = 'ME' or kind = 'ST' or kind = 'TO' or kind = 'TS' or kind = 'VO'
	)
group by locality, region, country;

/*
40. Average number of deaths caused by hurricanes.
*/

select avg(number)
from HumanImpact
where crisis_id in (
	select id
	from Crisis
	where kind = 'HU'
	)
	and (type = 'Death' or type = "Dead" or type = "Deaths");


/*
41. Total number of deaths caused by terrorist attacks
*/

Select sum(number)
From HumanImpact
Where crisis_id in (
	Select id
	From Crisis
	Where kind="TA");

/*
42. List of Hurricanes in the US that Wallace Stickney (WStickney) helped out with.
*/

select id
from Crisis
where kind = "HU" and id in(select entity_id
from Location where country="United States" or country = "United States of America" or country = "US" or country = "USA")
and id in(select id_crisis
from CrisisOrganization
where id_organization in (select id_organization
from OrganizationPerson
where id_person = "WStickney"));

/*
43. List of hurricanes in the US where FEMA was NOT involved.
*/

select id 
from Crisis
where kind = "HU" and id in(select entity_id
  from Location where country="United States" or country = "United States of America" )
      and id not in (select distinct id_crisis 
                from CrisisOrganization
                where id_organization = "FEMA");

/*
44. Number of crises that intelligence agencies were involved in.
*/

select count(*)
from CrisisOrganization
where id_organization in (
	select id
	from Organization
	where kind = 'IA'
	);

/*
45. How many more orgs does America have than Britain. 
*/

create temporary table US_ORG_count2 as 
	select count(*) as count
	from Organization
	where (country="United States" or country = "United States of America" or country = "US" or country = "USA");
	
create temporary table UK_ORG_count2 as
	select count(*) as count
	from Organization
	where (country="United Kingdom" or country = "UK");
	
select (US_ORG_count2.count - UK_ORG_count2.count)
from UK_ORG_count2 cross join US_ORG_count2;




















