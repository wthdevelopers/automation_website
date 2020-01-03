from flask import current_app as app
from flask import jsonify, request
import datetime


def _event_delete_one():
    """
    Edits one activity into the duty roster used by the ocomm 
    """

    roster_id_to_delete = request.args.get("event_id")

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "DELETE FROM duty_roster_comm WHERE roster_id='{0}'".format(roster_id_to_delete)
    with connection.cursor() as cursor:
        cursor.execute(query)

    query = "DELETE FROM duty_roster WHERE roster_id='{0}'".format(roster_id_to_delete)
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "done"
