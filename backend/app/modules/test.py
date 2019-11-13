from flask import request, url_for, jsonify, Blueprint
from flask_api import FlaskAPI, status, exceptions


module = Blueprint("test", __name__)

# logic that services the API
# to access request body/request query parameters, use the request module in flask
def _test():
    return jsonify({"test message": "hello"})

# routes and methods for this API is stated here
module.add_url_rule("/test", view_func=_test, methods=["GET"])
