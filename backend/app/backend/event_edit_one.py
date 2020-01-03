from flask import current_app as app
from flask import jsonify, request
import datetime


def _event_edit_one():
    """
    Edits one activity into the duty roster used by the ocomm 
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
    updated_duty_roster_activity = request.json["schedule_editor/edit_one"]

    activity_name = updated_duty_roster_activity["event_name"]
    start_datetime = generate_datetime(updated_duty_roster_activity["event_time"]["start_time"], updated_duty_roster_activity["event_time"]["start_date"])
    end_datetime = generate_datetime(updated_duty_roster_activity["event_time"]["end_time"], updated_duty_roster_activity["event_time"]["end_date"])
    place = updated_duty_roster_activity["event_location"]
    description = updated_duty_roster_activity["event_description"]

    ocomm_on_duty = updated_duty_roster_activity["ocomm_on_duty"]

    query = "UPDATE duty_roster \
        SET \
            activity_name='{0}', \
            start_datetime='{1}', \
            end_datetime='{2}', \
            place='{3}', \
            description='{4}' \
        WHERE roster_id='{5}';".format(activity_name, start_datetime, end_datetime, place, description, old_roster_id)
    with connection.cursor() as cursor:
        cursor.execute(query)

    query = "DELETE FROM duty_roster_comm WHERE roster_id='{0}'".format(old_roster_id)
    with connection.cursor() as cursor:
        cursor.execute(query)

    for ocomm_id in ocomm_on_duty:
        query = "INSERT INTO duty_roster_comm (comm_id, roster_id) VALUES ('{0}', '{1}')".format(ocomm_id, old_roster_id)
        with connection.cursor() as cursor:
            cursor.execute(query)

    return "done"

