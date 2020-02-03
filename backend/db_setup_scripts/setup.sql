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
      	`registered` BOOLEAN NOT NULL, \
      	`DoB` datetime NOT NULL, \
      	`gender` TEXT NOT NULL, \
      	`nationality` TEXT NOT NULL, \
      	`organisation` TEXT NOT NULL, \
      	`designation` TEXT NOT NULL, \
      	`dietary_pref` TEXT NOT NULL, \
      	`NoK_name` TEXT NOT NULL, \
      	`NoK_relationship` TEXT NOT NULL, \
      	`NoK_contact_number` TEXT NOT NULL, \
	`shirt_size` TEXT NOT NULL, \
	`previous_hackathons_attended` TEXT NOT NULL, \
	`bringing_utensils` TEXT NOT NULL, \
	`team_allocation_preference` TEXT NOT NULL, \
	`utensil_color` TEXT, \
        PRIMARY KEY(user_id) \
);
create trigger user_trigger before insert on `user` for each row set @last_uuid=uuid(), NEW.user_id=@last_uuid;

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
        `space` text, \
	`hack_submitted` tinyint NOT NULL default 0, \
        PRIMARY KEY(group_id) \
);
create trigger group_trigger before insert on `group` for each row set @last_uuid=uuid(), NEW.group_id=@last_uuid;

create table `tool` ( \
        `tool_id` varchar(36) NOT NULL, \
        `loaned` tinyint NOT NULL, \
        `name` text NOT NULL, \
        `description` text, \
	`latest_loan` varchar(36), \
        PRIMARY KEY(tool_id) \
);
create trigger tool_trigger before insert on `tool` for each row set @last_uuid=uuid(), NEW.tool_id=@last_uuid;

create table `loan` ( \
	`loan_id` varchar(36) NOT NULL, \
	`tool_id` varchar(36) NOT NULL, \
        `loan_to_group_id` varchar(36) NOT NULL, \
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

create table `category_user`( \
        `category_user_id` varchar(36) NOT NULL, \
        `category_id` varchar(36) NOT NULL, \
        `user_id` varchar(36) NOT NULL, \
        PRIMARY KEY(category_user_id) \
);
create trigger category_user_trigger before insert on `category_user` for each row set @last_uuid=uuid(), NEW.category_user_id=@last_uuid;

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
-- score will not have a trigger. it relies on an external file's input and hence will retain the score_id from that file

create table `judge`( \
        `judge_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(judge_id) \
);
-- judge will not have a trigger. it relies on an external file's input and hence will retain the judge_id from that file

create table `credentials`(
	`username` TEXT NOT NULL, \
	`password` varchar(256) NOT NULL \
);

create table `_user_preference_technology_of_interest` ( \
        `technology_of_interest_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(technology_of_interest_id) \
);
create trigger _user_preference_technology_of_interest_trigger before insert on `_user_preference_technology_of_interest` for each row set @last_uuid=uuid(), NEW.technology_of_interest_id=@last_uuid;

create table `_user_preference_technology_of_interest_user` ( \
        `technology_of_interest_user_id` varchar(36) NOT NULL, \
        `technology_of_interest_id` varchar(36) NOT NULL, \
        `user_id` varchar(36) NOT NULL, \
        PRIMARY KEY(technology_of_interest_user_id) \
);
create trigger _user_preference_technology_of_interest_user_trigger before insert on `_user_preference_technology_of_interest_user` for each row set @last_uuid=uuid(), NEW.technology_of_interest_user_id=@last_uuid;

create table `_user_preference_skills` ( \
        `skills_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(skills_id) \
);
create trigger _user_preference_skills_trigger before insert on `_user_preference_skills` for each row set @last_uuid=uuid(), NEW.skills_id=@last_uuid;

create table `_user_preference_skills_user` ( \
        `skills_user_id` varchar(36) NOT NULL, \
        `skills_id` varchar(36), \
        `other_skills` TEXT, \
        `user_id` varchar(36) NOT NULL, \
        PRIMARY KEY(skills_user_id) \
);
create trigger _user_preference_skills_user_trigger before insert on `_user_preference_skills_user` for each row set @last_uuid=uuid(), NEW.skills_user_id=@last_uuid;

create table `_user_preference_utensil_name`( \
        `utensil_name_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(utensil_name_id) \
);
create trigger _user_preference_utensil_name_trigger before insert on `_user_preference_utensil_name` for each row set @last_uuid=uuid(), NEW.utensil_name_id=@last_uuid;

create table `_user_preference_utensil_name_user`( \
        `utensil_name_user_id` varchar(36) NOT NULL, \
        `utensil_name_id` varchar(36) NOT NULL, \
        `user_id` varchar(36) NOT NULL, \
        PRIMARY KEY(utensil_name_user_id) \
);
create trigger _user_preference_utensil_name_user_trigger before insert on `_user_preference_utensil_name_user` for each row set @last_uuid=uuid(), NEW.utensil_name_user_id=@last_uuid;

create table `_user_preference_workshops` ( \
        `workshops_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(workshops_id) \
);
create trigger _user_preference_workshops_trigger before insert on `_user_preference_workshops` for each row set @last_uuid=uuid(), NEW.workshops_id=@last_uuid;

create table `_user_preference_workshops_user` ( \
        `workshops_user_id` varchar(36) NOT NULL, \
        `workshops_id` varchar(36) NOT NULL, \
        `user_id` varchar(36) NOT NULL, \
	`level_of_preference` INT NOT NULL, \
        PRIMARY KEY(workshops_user_id) \
);
create trigger _user_preference_workshops_user_trigger before insert on `_user_preference_workshops_user` for each row set @last_uuid=uuid(), NEW.workshops_user_id=@last_uuid;



-- create tables for wthack_automation_test
use wthack_automation_test;
create table `user` ( \
        `user_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        `contact_number` TEXT NOT NULL, \
        `email` TEXT NOT NULL, \
        `group_id` varchar(36), \
        `registered` BOOLEAN NOT NULL, \
        `DoB` datetime NOT NULL, \
        `gender` TEXT NOT NULL, \
        `nationality` TEXT NOT NULL, \
        `organisation` TEXT NOT NULL, \
        `designation` TEXT NOT NULL, \
        `dietary_pref` TEXT NOT NULL, \
        `NoK_name` TEXT NOT NULL, \
        `NoK_relationship` TEXT NOT NULL, \
        `NoK_contact_number` TEXT NOT NULL, \
        `shirt_size` TEXT NOT NULL, \
        `previous_hackathons_attended` TEXT NOT NULL, \
        `bringing_utensils` TEXT NOT NULL, \
        `team_allocation_preference` TEXT NOT NULL, \
        `utensil_color` TEXT, \
        PRIMARY KEY(user_id) \
);

create trigger user_trigger before insert on `user` for each row set @last_uuid=uuid(), NEW.user_id=@last_uuid;

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
        `space` text, \
	`hack_submitted` tinyint NOT NULL default 0, \
        PRIMARY KEY(group_id) \
);
create trigger group_trigger before insert on `group` for each row set @last_uuid=uuid(), NEW.group_id=@last_uuid;

create table `tool` ( \
        `tool_id` varchar(36) NOT NULL, \
        `loaned` tinyint NOT NULL, \
        `name` text NOT NULL, \
        `description` text, \
	`latest_loan` varchar(36), \
        PRIMARY KEY(tool_id) \
);
create trigger tool_trigger before insert on `tool` for each row set @last_uuid=uuid(), NEW.tool_id=@last_uuid;

create table `loan` ( \
	`loan_id` varchar(36) NOT NULL, \
	`tool_id` varchar(36) NOT NULL, \
        `loan_to_group_id` varchar(36) NOT NULL, \
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

create table `category_user`( \
        `category_user_id` varchar(36) NOT NULL, \
        `category_id` varchar(36) NOT NULL, \
        `user_id` varchar(36) NOT NULL, \
        PRIMARY KEY(category_user_id) \
);
create trigger category_user_trigger before insert on `category_user` for each row set @last_uuid=uuid(), NEW.category_user_id=@last_uuid;

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
-- score will not have a trigger. it relies on an external file's input and hence will retain the score_id from that file

create table `judge`( \
        `judge_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(judge_id) \
);
-- judge will not have a trigger. it relies on an external file's input and hence will retain the judge_id from that file

create table `credentials`(
        `username` TEXT NOT NULL, \
        `password` varchar(256) NOT NULL \
);

create table `_user_preference_technology_of_interest` ( \
        `technology_of_interest_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(technology_of_interest_id) \
);
create trigger _user_preference_technology_of_interest_trigger before insert on `_user_preference_technology_of_interest` for each row set @last_uuid=uuid(), NEW.technology_of_interest_id=@last_uuid;

create table `_user_preference_technology_of_interest_user` ( \
        `technology_of_interest_user_id` varchar(36) NOT NULL, \
        `technology_of_interest_id` varchar(36) NOT NULL, \
        `user_id` varchar(36) NOT NULL, \
        PRIMARY KEY(technology_of_interest_user_id) \
);
create trigger _user_preference_technology_of_interest_user_trigger before insert on `_user_preference_technology_of_interest_user` for each row set @last_uuid=uuid(), NEW.technology_of_interest_user_id=@last_uuid;

create table `_user_preference_skills` ( \
        `skills_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(skills_id) \
);
create trigger _user_preference_skills_trigger before insert on `_user_preference_skills` for each row set @last_uuid=uuid(), NEW.skills_id=@last_uuid;

create table `_user_preference_skills_user` ( \
        `skills_user_id` varchar(36) NOT NULL, \
        `skills_id` varchar(36), \
	`other_skills` TEXT, \
        `user_id` varchar(36) NOT NULL, \
        PRIMARY KEY(skills_user_id) \
);
create trigger _user_preference_skills_user_trigger before insert on `_user_preference_skills_user` for each row set @last_uuid=uuid(), NEW.skills_user_id=@last_uuid;

create table `_user_preference_utensil_name`( \
        `utensil_name_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(utensil_name_id) \
);
create trigger _user_preference_utensil_name_trigger before insert on `_user_preference_utensil_name` for each row set @last_uuid=uuid(), NEW.utensil_name_id=@last_uuid;

create table `_user_preference_utensil_name_user`( \
        `utensil_name_user_id` varchar(36) NOT NULL, \
        `utensil_name_id` varchar(36) NOT NULL, \
        `user_id` varchar(36) NOT NULL, \
        PRIMARY KEY(utensil_name_user_id) \
);
create trigger _user_preference_utensil_name_user_trigger before insert on `_user_preference_utensil_name_user` for each row set @last_uuid=uuid(), NEW.utensil_name_user_id=@last_uuid;

create table `_user_preference_workshops` ( \
        `workshops_id` varchar(36) NOT NULL, \
        `name` TEXT NOT NULL, \
        PRIMARY KEY(workshops_id) \
);
create trigger _user_preference_workshops_trigger before insert on `_user_preference_workshops` for each row set @last_uuid=uuid(), NEW.workshops_id=@last_uuid;

create table `_user_preference_workshops_user` ( \
        `workshops_user_id` varchar(36) NOT NULL, \
        `workshops_id` varchar(36) NOT NULL, \
        `user_id` varchar(36) NOT NULL, \
        `level_of_preference` INT NOT NULL, \
        PRIMARY KEY(workshops_user_id) \
);
create trigger _user_preference_workshops_user_trigger before insert on `_user_preference_workshops_user` for each row set @last_uuid=uuid(), NEW.workshops_user_id=@last_uuid;
