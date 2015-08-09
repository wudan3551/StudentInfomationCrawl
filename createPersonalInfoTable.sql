use StudentInfo;
create table personalInfo(id int PRIMARY KEY,
			  name varchar(20) character set utf8 not null,
			  Sex varchar(10) character set utf8 not null,
			  HomeTown varchar(20) character set utf8 not null,
			  BirthYear varchar(20) character set utf8 not null,
			  Nation varchar(20) character set utf8 not null,
			  RollDate date not null,
			  Source varchar(30) character set utf8 not null
			  );
show tables;
