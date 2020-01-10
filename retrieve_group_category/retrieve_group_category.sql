USE wthack_automation;

SELECT * FROM `group` INTO OUTFILE '/var/lib/mysql-files/group_export.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

SELECT * FROM competition_category INTO OUTFILE '/var/lib/mysql-files/category_export.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

SELECT * FROM category_group INTO OUTFILE '/var/lib/mysql-files/category_group_export.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
