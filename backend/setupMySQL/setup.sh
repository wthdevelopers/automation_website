#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH

cp "${SCRIPTPATH}/sampleData/comm.csv" /var/lib/mysql-files/sampleData/comm.csv
cp "${SCRIPTPATH}/sampleData/event-comm.csv" /var/lib/mysql-files/sampleData/event-comm.csv
cp "${SCRIPTPATH}/sampleData/event.csv" /var/lib/mysql-files/sampleData/event.csv
cp "${SCRIPTPATH}/sampleData/grp.csv" /var/lib/mysql-files/sampleData/grp.csv
cp "${SCRIPTPATH}/sampleData/tool.csv" /var/lib/mysql-files/sampleData/tool.csv
cp "${SCRIPTPATH}/sampleData/user.csv" /var/lib/mysql-files/sampleData/user.csv
mysql -u ubuntu -p < "${SCRIPTPATH}/setup.sql"
