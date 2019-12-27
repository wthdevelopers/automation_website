#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH


# set up sample tables
mysql -u root -p < "${SCRIPTPATH}/setup_backend_tests.sql"

