#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH

apt-get update

# installing dependencies for mysql
apt-get install -y mysql-server

# activate virtual environment and install dependencies
apt-get install -y python3-venv
sudo -u xubuntu python3 -m venv "${SCRIPTPATH}/../venvBackend"
# source "${SCRIPTPATH}/venvBackend/bin/activate"
# pip3 install -r "${SCRIPTPATH}/requirements.txt"

# setup demo data in mysql
"${SCRIPTPATH}/setupMySQL/setup.sh"
