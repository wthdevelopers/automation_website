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
create table `user` ( \
        `user_id` varchar(36) NOT NULL, \
      	`name` TEXT NOT NULL, \
      	`contact_number` TEXT NOT NULL, \
      	`email` TEXT NOT NULL, \
      	`group_id` varchar(36), \
      	`participating` tinyint NOT NULL, \
      	`DoB` datetime NOT NULL, \
      	`gender` TEXT NOT NULL, \
      	`nationality` TEXT NOT NULL, \
      	`category_of_interest` TEXT NOT NULL, \
      	`technology_of_interest` TEXT NOT NULL, \
      	`skills` TEXT NOT NULL, \
      	`organisation` TEXT NOT NULL, \
      	`designation` TEXT NOT NULL, \
      	`dietary_pref` TEXT NOT NULL, \
      	`NoK_name` TEXT NOT NULL, \
      	`NoK_relationship` TEXT NOT NULL, \
      	`NoK_contact_number` TEXT NOT NULL, \
        PRIMARY KEY(user_id) \
);
create trigger user_trigger before insert on `user` for each row set @last_uuid=uuid(), NEW.user_id=@last_uuid;

create table `duty_roster` ( \
          `roster_id` varchar(36) NOT NULL, \
          `activity_name` text NOT NULL, \
          `start_datetime` datetime NOT NULL, \
          `end_datetime` datetime NOT NULL, \
          `place` text NOT NULL, \
          `description` text, \
          PRIMARY KEY(roster_id) \
);
create trigger duty_roster_trigger before insert on `duty_roster` for each row set @last_uuid=uuid(), NEW.roster_id=@last_uuid;

create table `comm` (
        `comm_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        `contact` TEXT NOT NULL, \
        PRIMARY KEY (comm_id) \
);
create trigger comm_trigger before insert on `comm` for each row set @last_uuid=uuid(), NEW.comm_id=@last_uuid;

create table `duty_roster_comm` (
	`duty_roster_comm_id` varchar(36) NOT NULL, \
        `comm_id` varchar(36) NOT NULL, \
	`roster_id` varchar(36) NOT NULL, \
        PRIMARY KEY (comm_id) \
);
create trigger duty_roster_comm_trigger before insert on `duty_roster_comm` for each row set @last_uuid=uuid(), NEW.duty_roster_comm_id=@last_uuid;

create table `event` (
          `event_id` varchar(36) NOT NULL, \
          `name` TEXT NOT NULL, \
          `place` TEXT NOT NULL, \
          `start_datetime` datetime NOT NULL, \
          `end_datetime` datetime NOT NULL, \
          `description` text, \
          PRIMARY KEY(event_id) \
);
create trigger event_trigger before insert on `event` for each row set @last_uuid=uuid(), NEW.event_id=@last_uuid;

create table `consumable` ( \
          `consumable_id` varchar(36) NOT NULL, \
          `name` TEXT NOT NULL, \
          `description` TEXT, \
          `stock_qty` INT NOT NULL, \
          `total_qty` INT NOT NULL, \
          `quota_per_group` INT NOT NULL, \
          PRIMARY KEY(consumable_id) \
);
create trigger consumable_trigger before insert on `consumable` for each row set @last_uuid=uuid(), NEW.consumable_id=@last_uuid;

create table `consumable_group` ( \
          `consumable_group_id` varchar(36) NOT NULL, \
          `group_id` varchar(36) NOT NULL, \
          `consumable_id` varchar(36) NOT NULL, \
          `qty` INT NOT NULL, \
          PRIMARY KEY(consumable_group_id) \
);
create trigger consumable_group_trigger before insert on `consumable_group` for each row set @last_uuid=uuid(), NEW.consumable_group_id=@last_uuid;

create table `group` ( \
          `group_id` varchar(36) NOT NULL, \
          `name` text NOT NULL, \
          `space` text NOT NULL, \
          `categories` text NOT NULL, \
          PRIMARY KEY(group_id) \
);
create trigger group_trigger before insert on `group` for each row set @last_uuid=uuid(), NEW.group_id=@last_uuid;

create table `tool` ( \
          `tool_id` varchar(36) NOT NULL, \
          `status` TEXT NOT NULL, \
          `name` text NOT NULL, \
          `description` text, \
	  `latest_loan` varchar(36), \
          PRIMARY KEY(tool_id) \
);
create trigger tool_trigger before insert on `tool` for each row set @last_uuid=uuid(), NEW.tool_id=@last_uuid;

create table `loan` ( \
	`loan_id` varchar(36) NOT NULL, \
	`tool_id` varchar(36) NOT NULL, \
        `loan_to_user_id` varchar(36) NOT NULL, \
        `loan_datetime` datetime NOT NULL, \
	PRIMARY KEY (loan_id) \
);
create trigger loan_trigger before insert on `loan` for each row set @last_uuid=uuid(), NEW.loan_id=@last_uuid;

create table `competition_category`( \
          `category_id` varchar(36) NOT NULL, \
          `name` TEXT NOT NULL, \
          PRIMARY KEY(category_id) \
);
create trigger competition_category_trigger before insert on `competition_category` for each row set @last_uuid=uuid(), NEW.category_id=@last_uuid;

create table `category_group`( \
          `category_group_id` varchar(36) NOT NULL, \
          `category_id` varchar(36) NOT NULL, \
          `group_id` varchar(36) NOT NULL, \
          PRIMARY KEY(category_group_id) \
);
create trigger category_group_trigger before insert on `category_group` for each row set @last_uuid=uuid(), NEW.category_group_id=@last_uuid;

create table `score`( \
      	`score_id` varchar(36) NOT NULL, \
        `category_id` varchar(36) NOT NULL, \
      	`judge_id` varchar(36) NOT NULL, \
        `group_id` varchar(36) NOT NULL, \
      	`category_1_score` INT NOT NULL, \
      	`category_2_score` INT NOT NULL, \
      	`category_3_score` INT NOT NULL, \
      	`category_4_score` INT NOT NULL, \
        PRIMARY KEY(score_id) \
);
create trigger score_trigger before insert on `score` for each row set @last_uuid=uuid(), NEW.score_id=@last_uuid;



-- create tables for wthack_automation_test
use wthack_automation_test;
create table `user` ( \
        `user_id` varchar(36) NOT NULL, \
      	`name` TEXT NOT NULL, \
      	`contact_number` TEXT NOT NULL, \
      	`email` TEXT NOT NULL, \
      	`group_id` varchar(36), \
      	`participating` tinyint NOT NULL, \
      	`DoB` datetime NOT NULL, \
      	`gender` TEXT NOT NULL, \
      	`nationality` TEXT NOT NULL, \
      	`category_of_interest` TEXT NOT NULL, \
      	`technology_of_interest` TEXT NOT NULL, \
      	`skills` TEXT NOT NULL, \
      	`organisation` TEXT NOT NULL, \
      	`designation` TEXT NOT NULL, \
      	`dietary_pref` TEXT NOT NULL, \
      	`NoK_name` TEXT NOT NULL, \
      	`NoK_relationship` TEXT NOT NULL, \
      	`NoK_contact_number` TEXT NOT NULL, \
        PRIMARY KEY(user_id) \
);
create trigger user_trigger before insert on `user` for each row set @last_uuid=uuid(), NEW.user_id=@last_uuid;

create table `duty_roster` ( \
          `roster_id` varchar(36) NOT NULL, \
          `activity_name` text NOT NULL, \
          `start_datetime` datetime NOT NULL, \
          `end_datetime` datetime NOT NULL, \
          `place` text NOT NULL, \
          `description` text, \
          PRIMARY KEY(roster_id) \
);
create trigger duty_roster_trigger before insert on `duty_roster` for each row set @last_uuid=uuid(), NEW.roster_id=@last_uuid;

create table `comm` (
        `comm_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        `contact` TEXT NOT NULL, \
        PRIMARY KEY (comm_id) \
);
create trigger comm_trigger before insert on `comm` for each row set @last_uuid=uuid(), NEW.comm_id=@last_uuid;

create table `duty_roster_comm` (
	`duty_roster_comm_id` varchar(36) NOT NULL, \
        `comm_id` varchar(36) NOT NULL, \
	`roster_id` varchar(36) NOT NULL, \
        PRIMARY KEY (comm_id) \
);
create trigger duty_roster_comm_trigger before insert on `duty_roster_comm` for each row set @last_uuid=uuid(), NEW.duty_roster_comm_id=@last_uuid;

create table `event` (
          `event_id` varchar(36) NOT NULL, \
          `name` TEXT NOT NULL, \
          `place` TEXT NOT NULL, \
          `start_datetime` datetime NOT NULL, \
          `end_datetime` datetime NOT NULL, \
          `description` text, \
          PRIMARY KEY(event_id) \
);
create trigger event_trigger before insert on `event` for each row set @last_uuid=uuid(), NEW.event_id=@last_uuid;

create table `consumable` ( \
          `consumable_id` varchar(36) NOT NULL, \
          `name` TEXT NOT NULL, \
          `description` TEXT, \
          `stock_qty` INT NOT NULL, \
          `total_qty` INT NOT NULL, \
          `quota_per_group` INT NOT NULL, \
          PRIMARY KEY(consumable_id) \
);
create trigger consumable_trigger before insert on `consumable` for each row set @last_uuid=uuid(), NEW.consumable_id=@last_uuid;

create table `consumable_group` ( \
          `consumable_group_id` varchar(36) NOT NULL, \
          `group_id` varchar(36) NOT NULL, \
          `consumable_id` varchar(36) NOT NULL, \
          `qty` INT NOT NULL, \
          PRIMARY KEY(consumable_group_id) \
);
create trigger consumable_group_trigger before insert on `consumable_group` for each row set @last_uuid=uuid(), NEW.consumable_group_id=@last_uuid;

create table `group` ( \
          `group_id` varchar(36) NOT NULL, \
          `name` text NOT NULL, \
          `space` text NOT NULL, \
          `categories` text NOT NULL, \
          PRIMARY KEY(group_id) \
);
create trigger group_trigger before insert on `group` for each row set @last_uuid=uuid(), NEW.group_id=@last_uuid;

create table `tool` ( \
          `tool_id` varchar(36) NOT NULL, \
          `status` TEXT NOT NULL, \
          `name` text NOT NULL, \
          `description` text, \
	  `latest_loan` varchar(36), \
          PRIMARY KEY(tool_id) \
);
create trigger tool_trigger before insert on `tool` for each row set @last_uuid=uuid(), NEW.tool_id=@last_uuid;

create table `loan` ( \
	`loan_id` varchar(36) NOT NULL, \
	`tool_id` varchar(36) NOT NULL, \
        `loan_to_user_id` varchar(36) NOT NULL, \
        `loan_datetime` datetime NOT NULL, \
	PRIMARY KEY (loan_id) \
);
create trigger loan_trigger before insert on `loan` for each row set @last_uuid=uuid(), NEW.loan_id=@last_uuid;

create table `competition_category`( \
          `category_id` varchar(36) NOT NULL, \
          `name` TEXT NOT NULL, \
          PRIMARY KEY(category_id) \
);
create trigger competition_category_trigger before insert on `competition_category` for each row set @last_uuid=uuid(), NEW.category_id=@last_uuid;

create table `category_group`( \
          `category_group_id` varchar(36) NOT NULL, \
          `category_id` varchar(36) NOT NULL, \
          `group_id` varchar(36) NOT NULL, \
          PRIMARY KEY(category_group_id) \
);
create trigger category_group_trigger before insert on `category_group` for each row set @last_uuid=uuid(), NEW.category_group_id=@last_uuid;

create table `score`( \
      	`score_id` varchar(36) NOT NULL, \
        `category_id` varchar(36) NOT NULL, \
      	`judge_id` varchar(36) NOT NULL, \
        `group_id` varchar(36) NOT NULL, \
      	`category_1_score` INT NOT NULL, \
      	`category_2_score` INT NOT NULL, \
      	`category_3_score` INT NOT NULL, \
      	`category_4_score` INT NOT NULL, \
        PRIMARY KEY(score_id) \
);
create trigger score_trigger before insert on `score` for each row set @last_uuid=uuid(), NEW.score_id=@last_uuid;

