from flask import current_app as app
from flask import jsonify, request
import flask_login, pymysql


@flask_login.login_required
def _participants_ID_register(id):
    """
    Registers an existing participant
    """
    query = "UPDATE user SET registered=1 WHERE user_id='{0}'".format(pymysql.escape_string(id))
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.close()

    return {"success": "ok"}, 200

