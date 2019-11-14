create database wthack_automation;
use wthack_automation;

create table `user` (`uid` varchar(36), `name` TEXT, `contact_number` TEXT, `email` TEXT, `gid` varchar(36), `participating` tinyint);
load data infile './user.csv' into table `user` ignore 1 lines;
create trigger user_trigger before insert on `user` for each row set NEW.uid=uuid();

create table `grp` (`gid` varchar(36), `gname` text, `space` text, `categories` text);
load data infile './grp.csv' into table `grp` ignore 1 lines;
create trigger grp_trigger before insert on `grp` for each row set NEW.gid=uuid();

create table `tool` (`tid` varchar(36), `on_loan` tinyint, `on_loan_to` varchar(36), `due_date` datetime, `tool_name` text, `description` text);
load data infile './tool.csv' into table `tool` ignore 1 lines;
create trigger tool_trigger before insert on `tool` for each row set NEW.tid=uuid();

create table `event` (`eid` varchar(36), `name` text, `start` datetime, `end` datetime, `place` text, `description` text);
load data infile './event.csv' into table `event` ignore 1 lines;
create trigger event_trigger before insert on `event` for each row set NEW.eid=uuid();

create table `comm` (`cid` varchar(36), `name` text, `contact` text);
load data infile './comm.csv' into table `comm` ignore 1 lines;
create trigger comm_trigger before insert on `comm` for each row set NEW.cid=uuid();

create table `event-comm` (`ecid` varchar(36), `eid` varchar(36), `cid` varchar(36));
load data infile './event-comm.csv' into table `event-comm` ignore 1 lines;
create trigger `event-comm_trigger` before insert on `event-comm` for each row set NEW.ecid=uuid();
