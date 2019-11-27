#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH

# activate virtual environment and install dependencies
apt-get install -y python3-venv
# python3 -m venv "${SCRIPTPATH}/venvBackend"
# source "${SCRIPTPATH}/venvBackend/bin/activate"
# pip3 install -r "${SCRIPTPATH}/requirements.txt"

# setup demo data in mysql
"${SCRIPTPATH}/setupMySQL/setup.sh"
