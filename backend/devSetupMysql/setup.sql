create database wthack_automation;
use wthack_automation;


create table `user` (
	`uid` INT NOT NULL AUTO_INCREMENT,
	`name` TEXT, 
	`contact_number` TEXT, 
	`email` TEXT, 
	`gid` INT NOT NULL, 
	`participating` tinyint NOT NULL,
	PRIMARY KEY (uid)
);

LOAD DATA INFILE '/var/lib/mysql-files/sampleData/user.csv' INTO TABLE `user`
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;


create table `grp` (
	`gid` INT NOT NULL AUTO_INCREMENT, 
	`gname` TEXT, 
	`space` TEXT, 
	`categories` TEXT,
	PRIMARY KEY (gid)
);
load data infile '/var/lib/mysql-files/sampleData/grp.csv' into table `grp` 
fields terminated by ',' enclosed by '"'
lines terminated by '\n' ignore 1 lines;


create table `tool` (
	`tid` INT NOT NULL AUTO_INCREMENT, 
	`on_loan` tinyint, 
	`on_loan_to` INT, 
	`due_date` datetime, 
	`tool_name` TEXT, 
	`description` TEXT,
	PRIMARY KEY (tid)
);
load data infile '/var/lib/mysql-files/sampleData/tool.csv' into table `tool` 
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;


create table `event` (
	`eid` INT NOT NULL AUTO_INCREMENT, 
	`name` TEXT, 
	`start` datetime, 
	`end` datetime, 
	`place` TEXT, 
	`description` TEXT,
	PRIMARY KEY (eid)
);
load data infile '/var/lib/mysql-files/sampleData/event.csv' into table `event` 
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;


create table `comm` (
	`cid` INT NOT NULL AUTO_INCREMENT, 
	`name` TEXT, 
	`contact` TEXT,
	PRIMARY KEY (cid)
);
load data infile '/var/lib/mysql-files/sampleData/comm.csv' into table `comm` 
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;


create table `event-comm` (
	`ecid` INT NOT NULL AUTO_INCREMENT, 
	`eid` INT, 
	`cid` INT,
	PRIMARY KEY (ecid)
);
load data infile '/var/lib/mysql-files/sampleData/event-comm.csv' into table `event-comm` 
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;
