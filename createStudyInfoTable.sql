use StudentInfo;
create table StudyInfo(id int PRIMARY KEY,
		       name varchar(20) character set utf8 not null,
		       Sex varchar(10) character set utf8 not null,
		       LastSchool varchar(20) character set utf8 not null,
		       School varchar(20) character set utf8 not null,
		       Major varchar(20) character set utf8 not null,
		       Tutor varchar(20) character set utf8 not null,
		       ResearchDirection varchar(30) character set utf8 not null
		       );
show tables;
