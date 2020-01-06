from flask import current_app as app
from flask import jsonify, request
import datetime


def _event_edit_one():
    """
    Edits one activity into the schedule used by participants
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
    old_roster_id = request.args.get("event_id")
    updated_event_activity = request.json["event_edit_one"]

    activity_name = updated_event_activity["event_name"]
    start_datetime = generate_datetime(updated_event_activity["event_time"]["start_time"], updated_event_activity["event_time"]["start_date"])
    end_datetime = generate_datetime(updated_event_activity["event_time"]["end_time"], updated_event_activity["event_time"]["end_date"])
    place = updated_event_activity["event_location"]
    description = updated_event_activity["event_description"]

    query = "UPDATE event \
        SET \
            name='{0}', \
            start_datetime='{1}', \
            end_datetime='{2}', \
            place='{3}', \
            description='{4}' \
        WHERE event_id='{5}';".format(activity_name, start_datetime, end_datetime, place, description, old_roster_id)
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "done"

