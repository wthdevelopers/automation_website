import sys, os
from flask import request, url_for, jsonify, Blueprint
from flask_api import FlaskAPI, status, exceptions

dirname = os.path.dirname(__file__)
sys.path.append(dirname)

from upcoming_events import _upcoming_events
from find_participants import _find_participants
from ocomm_get_all import _ocomm_get_all
from participants_register import _participants_register


module = Blueprint("backend", __name__)

# routes and methods for this API is stated here
module.add_url_rule("/functions/upcoming_events", view_func=_upcoming_events, methods=["GET"])
module.add_url_rule("/functions/find_participants", view_func=_find_participants, methods=["GET"])
module.add_url_rule("/ocomm/get_all", view_func=_ocomm_get_all, methods=["GET"])
module.add_url_rule("/participants/register", view_func=_participants_register, methods=["PUT"])


