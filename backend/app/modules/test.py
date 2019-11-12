from flask import request, url_for, jsonify, Blueprint
from flask_api import FlaskAPI, status, exceptions


module = Blueprint("test", __name__)

def _test():
    return jsonify({"test message": "hello"})

module.add_url_rule("/test", view_func=_test, methods=["GET"])
