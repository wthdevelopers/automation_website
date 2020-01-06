from flask import current_app as app
from flask import jsonify, request
from datetime import timedelta


def _event_delay_multiple():
    """
    Delays multiple events by a specified number of minutes
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    request_body = request.json
    event_id_list = request_body["schedule_editor/delay"]["event_id_list"]
    delay_minutes = request_body["schedule_editor/delay"]["delay_by_minutes"]

    for each_activity_id in event_id_list:

        query = "SELECT start_datetime, end_datetime FROM event WHERE event_id='{0}';".format(each_activity_id)
        with connection.cursor() as cursor:
            cursor.execute(query)
            query_result = cursor.fetchall()

        new_start_datetime = query_result[0]["start_datetime"] + timedelta(minutes=delay_minutes)
        new_end_datetime = query_result[0]["end_datetime"] + timedelta(minutes=delay_minutes)

        query = "UPDATE event SET start_datetime='{0}', end_datetime='{1}' WHERE event_id='{2}';".format(new_start_datetime, new_end_datetime, each_activity_id)
        with connection.cursor() as cursor:
            cursor.execute(query)

    return "done"
