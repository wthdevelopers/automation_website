#!/bin/bash

cp sampleData/comm.csv /var/lib/mysql-files/sampleData/comm.csv
cp sampleData/event-comm.csv /var/lib/mysql-files/sampleData/event-comm.csv
cp sampleData/event.csv /var/lib/mysql-files/sampleData/event.csv
cp sampleData/grp.csv /var/lib/mysql-files/sampleData/grp.csv
cp sampleData/tool.csv /var/lib/mysql-files/sampleData/tool.csv
cp sampleData/user.csv /var/lib/mysql-files/sampleData/user.csv
mysql -u ubuntu -p < setup.sql
