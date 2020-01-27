from flask import current_app as app
from flask import jsonify, request
import flask_login


@flask_login.login_required
def _loans_return_ID(tool_id):
    """
    Returns a tool from a specific group
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "UPDATE tool SET loaned='0' WHERE tool_id='{0}'".format(tool_id)
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "OK", 200
