create database wthack_automation;
create database wthack_automation_test;

/*
CREATE USER 'ubuntu'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON wthack_automation.* TO 'ubuntu'@'localhost';
*/
-- default mysql configurations
UPDATE mysql.user SET authentication_string=PASSWORD('password') WHERE User='root';  -- set root password
DELETE FROM mysql.user WHERE User='';  -- remove anonymous users
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');  -- root can only connect locally
DROP DATABASE IF EXISTS test;  -- drop test db
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';

-- create user for remote connection
GRANT ALL PRIVILEGES ON wthack_automation.* TO 'remote'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON wthack_automation_test.* TO 'remote'@'%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;

-- create and fill up tables for wthack_automation
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

LOAD DATA INFILE '/var/lib/mysql-files/user.csv' INTO TABLE `user`
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;


create table `grp` (
	`gid` INT NOT NULL AUTO_INCREMENT, 
	`gname` TEXT, 
	`space` TEXT, 
	`categories` TEXT,
	PRIMARY KEY (gid)
);
load data infile '/var/lib/mysql-files/grp.csv' into table `grp` 
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
load data infile '/var/lib/mysql-files/tool.csv' into table `tool` 
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
load data infile '/var/lib/mysql-files/event.csv' into table `event` 
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
load data infile '/var/lib/mysql-files/comm.csv' into table `comm` 
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
load data infile '/var/lib/mysql-files/event-comm.csv' into table `event-comm` 
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;


-- create tables for wthack_automation_test
create table `user` (
        `uid` INT NOT NULL AUTO_INCREMENT,
        `name` TEXT,
        `contact_number` TEXT,
        `email` TEXT,
        `gid` INT NOT NULL,
        `participating` tinyint NOT NULL,
        PRIMARY KEY (uid)
);

create table `grp` (
        `gid` INT NOT NULL AUTO_INCREMENT,
        `gname` TEXT,
        `space` TEXT,
        `categories` TEXT,
        PRIMARY KEY (gid)
);

create table `tool` (
        `tid` INT NOT NULL AUTO_INCREMENT,
        `on_loan` tinyint,
        `on_loan_to` INT,
        `due_date` datetime,
        `tool_name` TEXT,
        `description` TEXT,
        PRIMARY KEY (tid)
);

create table `event` (
        `eid` INT NOT NULL AUTO_INCREMENT,
        `name` TEXT,
        `start` datetime,
        `end` datetime,
        `place` TEXT,
        `description` TEXT,
        PRIMARY KEY (eid)
);

create table `comm` (
        `cid` INT NOT NULL AUTO_INCREMENT,
        `name` TEXT,
        `contact` TEXT,
        PRIMARY KEY (cid)
);

create table `event_comm` (
        `ecid` INT NOT NULL AUTO_INCREMENT,
        `eid` INT,
        `cid` INT,
        PRIMARY KEY (ecid)
);

