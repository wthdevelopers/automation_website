from flask import current_app as app
from flask import jsonify, request
import flask_login


# @flask_login.login_required
def _participants_ID_deregister(id):
    """
    Deregisters an existing participant
    """
    query = "UPDATE user SET registered=0 WHERE user_id='{0}'".format(id)
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "done.", 200

