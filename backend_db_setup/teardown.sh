#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

mysql -u root -p < "${SCRIPTPATH}/teardown.sql"
