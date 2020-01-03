from flask import current_app as app
from flask import jsonify, request
import datetime


def _event_add_one():
    """
    Adds one activity into the duty roster used by the ocomm 
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
    new_duty_roster_activity = request.json["schedule_editor/add"]

    activity_name = new_duty_roster_activity["event_name"]
    start_datetime = generate_datetime(new_duty_roster_activity["event_time"]["start_time"], new_duty_roster_activity["event_time"]["start_date"])
    end_datetime = generate_datetime(new_duty_roster_activity["event_time"]["end_time"], new_duty_roster_activity["event_time"]["end_date"])
    place = new_duty_roster_activity["event_location"]
    description = new_duty_roster_activity["event_description"]

    ocomm_on_duty = new_duty_roster_activity["ocomm_on_duty"]

    query = "INSERT INTO duty_roster (activity_name, start_datetime, end_datetime, place, description) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');".format(activity_name, start_datetime, end_datetime, place, description)
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.execute("SELECT @last_uuid;")
        new_duty_roster_id = cursor.fetchall()[0]["@last_uuid"]

    for ocomm_id in ocomm_on_duty:
        query = "INSERT INTO duty_roster_comm (comm_id, roster_id) VALUES ('{0}', '{1}')".format(ocomm_id, new_duty_roster_id)
        with connection.cursor() as cursor:
            cursor.execute(query)

    return "done"
