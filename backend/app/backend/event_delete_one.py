from flask import current_app as app
from flask import jsonify, request
import datetime


def _event_delete_one():
    """
    Edits one activity into the schedule for the participants
    """

    event_id_to_delete = request.args.get("event_id")

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "DELETE FROM event WHERE event_id='{0}'".format(event_id_to_delete)
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "done"
