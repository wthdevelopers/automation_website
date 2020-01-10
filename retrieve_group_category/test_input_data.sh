#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH

# copy files into authorized folder
# red: https://stackoverflow.com/questions/32737478/how-should-i-tackle-secure-file-priv-in-mysql
cp "${SCRIPTPATH}/test_group_data.csv" /var/lib/mysql-files/
cp "${SCRIPTPATH}/test_category_data.csv" /var/lib/mysql-files/
cp "${SCRIPTPATH}/test_category_group_data.csv" /var/lib/mysql-files/

mysql -u root -p < "${SCRIPTPATH}/test_input_data.sql"
