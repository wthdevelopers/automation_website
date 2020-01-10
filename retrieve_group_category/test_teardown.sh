#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH

# remove files from authorized folder
rm /var/lib/mysql-files/test_group_data.csv 
rm /var/lib/mysql-files/test_category_data.csv
rm /var/lib/mysql-files/test_category_group_data.csv

mysql -u root -p < "${SCRIPTPATH}/test_teardown.sql"
