from flask import current_app as app
from flask import jsonify, request
import flask_login, pymysql


@flask_login.login_required
def _participants_ID_ungiven_cash(id):
    """
    Changes the value of the column given_cash of db table user to 0
    """
    query = "UPDATE user SET given_cash=0 WHERE user_id='{0}'".format(pymysql.escape_string(id))
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.close()

    return {"success": "ok"}, 200

