from flask import current_app as app
from flask import jsonify, request
import datetime


def _event_add_one():
    """
    Adds one activity into the schedule viewed by participants
    """

    def generate_datetime(time, date):
        time = time.split(":")
        date = date.split("-")

        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        hour = int(time[0])
        minute = int(time[1])

        return datetime.datetime(year, month, day, hour, minute)

    connection = app.config["PYMYSQL_CONNECTION"]
    new_event_activity = request.json["schedule_editor/add"]

    activity_name = new_event_activity["event_name"]
    start_datetime = generate_datetime(new_event_activity["event_time"]["start_time"], new_event_activity["event_time"]["start_date"])
    end_datetime = generate_datetime(new_event_activity["event_time"]["end_time"], new_event_activity["event_time"]["end_date"])
    place = new_event_activity["event_location"]
    description = new_event_activity["event_description"]

    query = "INSERT INTO event (name, start_datetime, end_datetime, place, description) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');".format(activity_name, start_datetime, end_datetime, place, description)
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "done"
