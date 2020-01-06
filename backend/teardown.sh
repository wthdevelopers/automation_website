#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo "${SCRIPTPATH}"

# push any installed modules into requirements.txt and leave virtual environment
source "${SCRIPTPATH}/venvBackend/bin/activate"
pip3 freeze > "${SCRIPTPATH}/requirements.txt"
deactivate

# remove mysql db
"${SCRIPTPATH}/db_setup_scripts/teardown.sh"

# remove venvBackend folder
# rm -rf "${SCRIPTPATH}/venvBackend"
