#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH

cp "${SCRIPTPATH}/sampleData/comm.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/event-comm.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/event.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/grp.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/tool.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/user.csv" /var/lib/mysql-files
mysql -u root -p < "${SCRIPTPATH}/setup.sql"
