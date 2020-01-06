import sys, os
from flask import request, url_for, jsonify, Blueprint
from flask_api import FlaskAPI, status, exceptions

dirname = os.path.dirname(__file__)
sys.path.append(dirname)

from upcoming_events import _upcoming_events
from find_participants import _find_participants
from participants_register import _participants_register
from participants_get_one import _participants_get_one
from item_loans_get_all import _item_loans_get_all
from event_delay_multiple import _event_delay_multiple
from event_add_one import _event_add_one
from event_edit_one import _event_edit_one
from event_delete_one import _event_delete_one


module = Blueprint("backend", __name__)

# routes and methods for this API is stated here
module.add_url_rule("/functions/upcoming_events", view_func=_upcoming_events, methods=["GET"])
module.add_url_rule("/functions/find_participants", view_func=_find_participants, methods=["GET"])
module.add_url_rule("/participants/register", view_func=_participants_register, methods=["PUT"])
module.add_url_rule("/participants/get_one", view_func=_participants_get_one, methods=["GET"])
module.add_url_rule("/item_loans/get_all", view_func=_item_loans_get_all, methods=["GET"])
module.add_url_rule("/event/delay_multiple", view_func=_event_delay_multiple, methods=["PUT"])
module.add_url_rule("/event/add_one", view_func=_event_add_one, methods=["POST"])
module.add_url_rule("/event/edit_one", view_func=_event_edit_one, methods=["PUT"])
module.add_url_rule("/event/delete_one", view_func=_event_delete_one, methods=["DELETE"])


