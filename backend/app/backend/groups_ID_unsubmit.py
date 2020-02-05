from flask import current_app as app
from flask import jsonify, request
import flask_login


@flask_login.login_required
def _groups_ID_unsubmit(group_id):
    """
    Registers that the group has unsubmitted a hack
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "UPDATE `group` SET hack_submitted=0 WHERE group_id='{0}'".format(group_id)
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "OK", 200
