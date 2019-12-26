#!/bin/bash

# assuming that setup.sh has been ran, and there's already a virtual environment with the install packages
# activate the virtual environment
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo $SCRIPTPATH\

source "${SCRIPTPATH}/../venvBackend/bin/activate"
export FLASK_APP=wsgi.py
export FLASK_ENV=local
python3 -m flask run --port=5000
