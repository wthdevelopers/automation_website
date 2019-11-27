#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

mysql -u ubuntu -p < "${SCRIPTPATH}/teardown.sql"
