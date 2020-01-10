#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH

# remove files from authorized folder
rm /var/lib/mysql-files/judge_data.csv 
rm /var/lib/mysql-files/score_data.csv

mysql -u root -p < "${SCRIPTPATH}/teardown.sql"
