USE `wthack_automation`;

LOAD DATA LOCAL INFILE 'judge_data.csv' INTO TABLE judge
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(judge_id, name);

LOAD DATA LOCAL INFILE 'score_data.csv' INTO TABLE score
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(score_id, category_id, judge_id, `group_id`, category_1_score, category_2_score, category_3_score, category_4_score);

