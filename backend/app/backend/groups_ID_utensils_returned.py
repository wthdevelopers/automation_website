from flask import current_app as app
from flask import jsonify, request
import flask_login, pymysql


@flask_login.login_required
def _groups_ID_utensils_returned(id):
    """
    changes the column value utensils_returned of db table group to 1
    """
    query = "UPDATE `group` SET utensils_returned=1 WHERE group_id='{0}'".format(pymysql.escape_string(id))
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.close()

    return {"success": "ok"}, 200

