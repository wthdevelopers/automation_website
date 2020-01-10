#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH

mysql -u root -p < "${SCRIPTPATH}/retrieve_group_category.sql"

mv /var/lib/mysql-files/group_export.csv .
mv /var/lib/mysql-files/category_export.csv .
mv /var/lib/mysql-files/category_group_export.csv .
