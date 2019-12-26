import sys, os
from flask import request, url_for, jsonify, Blueprint
from flask_api import FlaskAPI, status, exceptions

dirname = os.path.dirname(__file__)
sys.path.append(dirname)
from upcoming_events import _upcoming_events


module = Blueprint("backend", __name__)

# routes and methods for this API is stated here
module.add_url_rule("/functions/upcoming_events", view_func=_upcoming_events, methods=["GET"])

