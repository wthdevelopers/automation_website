#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH

# copy files into authorized folder
# red: https://stackoverflow.com/questions/32737478/how-should-i-tackle-secure-file-priv-in-mysql
cp "${SCRIPTPATH}/judge_data.csv" /var/lib/mysql-files/
cp "${SCRIPTPATH}/score_data.csv" /var/lib/mysql-files/

mysql -u root -p < "${SCRIPTPATH}/input_data.sql"
