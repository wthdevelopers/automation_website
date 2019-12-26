#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH


# copy over the files that will be inserted into mysql server
cp "${SCRIPTPATH}/sampleData/comm.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/event-comm.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/event.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/grp.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/tool.csv" /var/lib/mysql-files
cp "${SCRIPTPATH}/sampleData/user.csv" /var/lib/mysql-files

# expose mysql-server to open internet
sed "s/bind-address		= 127.0.0.1/bind-address		= 0.0.0.0/g" "/etc/mysql/mysql.conf.d/mysqld.cnf" > "/etc/mysql/mysql.conf.d/mysqld.cnf"

# expose port 3306 to public
iptables -A INPUT -i eth0 -p tcp --destination-port 3306 -j ACCEPT

# run sql script
mysql -u root < "${SCRIPTPATH}/setup.sql"

/etc/init.d/mysql restart
