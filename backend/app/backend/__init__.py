import sys, os
from flask import request, url_for, jsonify, Blueprint, session
from flask_api import FlaskAPI, status, exceptions
import flask_login

dirname = os.path.dirname(__file__)
sys.path.append(dirname)

from participants_ID_register import _participants_ID_register
from participants_ID_deregister import _participants_ID_deregister
from participants_get_all import _participants_get_all
from participants_ID_alldata import _participants_ID_alldata
from participants_ID_update import _participants_ID_update
from participants_ID_group import _participants_ID_group
from participants_ID_given_cash import _participants_ID_given_cash
from participants_ID_ungiven_cash import _participants_ID_ungiven_cash
from tools_get_all import _tools_get_all
from loans_ID_loan_ID import _loans_ID_loan_ID
from loans_return_ID import _loans_return_ID
from groups_get_all import _groups_get_all
from groups_ID_alldata import _groups_ID_alldata
from groups_ID_update import _groups_ID_update
from groups_ID_update_members import _groups_ID_update_members
from groups_create import _groups_create
from groups_ID_submit import _groups_ID_submit
from groups_ID_unsubmit import _groups_ID_unsubmit
from groups_ID_utensils_returned import _groups_ID_utensils_returned
from groups_ID_utensils_loaned import _groups_ID_utensils_loaned

from auth import _login
from auth import _logout


module = Blueprint("backend", __name__)

@flask_login.login_required
def _test():
    print("test endpoint - session id: {0}".format(id(session)))
    print("test endpoint - current_user: {0}".format(flask_login.current_user))
    return "HELLO WORLD"


# routes and methods for this API is stated here
module.add_url_rule("/participants/<id>/register", view_func=_participants_ID_register, methods=["PUT"])
module.add_url_rule("/participants/<id>/deregister", view_func=_participants_ID_deregister, methods=["PUT"])
module.add_url_rule("/participants/get_all", view_func=_participants_get_all, methods=["GET"])
module.add_url_rule("/participants/<id>/alldata", view_func=_participants_ID_alldata, methods=["GET"])
module.add_url_rule("/participants/<id>/update", view_func=_participants_ID_update, methods=["PUT"])
module.add_url_rule("/participants/<id>/group", view_func=_participants_ID_group, methods=["GET"])
module.add_url_rule("/participants/<id>/given_cash", view_func=_participants_ID_given_cash, methods=["PUT"])
module.add_url_rule("/participants/<id>/ungiven_cash", view_func=_participants_ID_ungiven_cash, methods=["PUT"])
module.add_url_rule("/tools/get_all", view_func=_tools_get_all, methods=["GET"])
module.add_url_rule("/loans/<group_id>/loan/<tool_id>", view_func=_loans_ID_loan_ID, methods=["POST"])
module.add_url_rule("/loans/return/<tool_id>", view_func=_loans_return_ID, methods=["PUT"])
module.add_url_rule("/groups/get_all", view_func=_groups_get_all, methods=["GET"])
module.add_url_rule("/groups/<id>/alldata", view_func=_groups_ID_alldata, methods=["GET"])
module.add_url_rule("/groups/<id>/update", view_func=_groups_ID_update, methods=["PUT"])
module.add_url_rule("/groups/<id>/update_members", view_func=_groups_ID_update_members, methods=["PUT"])
module.add_url_rule("/groups/create", view_func=_groups_create, methods=["POST"])
module.add_url_rule("/groups/<group_id>/submit", view_func=_groups_ID_submit, methods=["PUT"])
module.add_url_rule("/groups/<group_id>/unsubmit", view_func=_groups_ID_unsubmit, methods=["PUT"])
module.add_url_rule("/groups/<id>/utensils_returned", view_func=_groups_ID_utensils_returned, methods=["PUT"])
module.add_url_rule("/groups/<id>/utensils_loaned", view_func=_groups_ID_utensils_loaned, methods=["PUT"])

module.add_url_rule("/login", view_func=_login, methods=["POST"])
module.add_url_rule("/logout", view_func=_logout, methods=["GET"])
module.add_url_rule("/test", view_func=_test, methods=["GET"])
