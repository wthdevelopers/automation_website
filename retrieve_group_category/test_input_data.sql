USE `wthack_automation`;

LOAD DATA LOCAL INFILE 'test_group_data.csv' INTO TABLE `group`
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`group_id`, name, space, categories);

LOAD DATA LOCAL INFILE 'test_category_data.csv' INTO TABLE competition_category
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(category_id, name);

LOAD DATA LOCAL INFILE 'test_category_group_data.csv' INTO TABLE category_group
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(category_group_id, category_id, `group_id`);

