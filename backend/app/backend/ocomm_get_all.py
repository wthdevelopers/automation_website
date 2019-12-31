from flask import current_app as app
from flask import jsonify, request

def _ocomm_get_all():
    """
    Returns information regarding all ocomm members and their current attending duty_roster
    """
    query_participant_name = request.args.get("participant_name")
    query = "SELECT \
            comm.comm_id as ocomm_id, \
            comm.name as ocomm_name, \
            comm.contact as ocomm_contact, \
            duty_roster.start_datetime as start_datetime, \
            duty_roster.end_datetime as end_datetime, \
            duty_roster.place as ocomm_current_location \
        FROM comm \
        INNER JOIN \
            duty_roster_comm ON comm.comm_id=duty_roster_comm.comm_id \
        INNER JOIN \
            duty_roster ON duty_roster_comm.roster_id=duty_roster.roster_id \
        WHERE CURDATE() BETWEEN DATE(duty_roster.start_datetime) AND DATE(duty_roster.end_datetime);"
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    # parse query output into formatted output
    output = {"find_ocomm": [], "_ocomm_count": 0}
    for each_entry in query_result:
        each_entry_output = {"ocomm_current_shift_time":{}}
        each_entry_output["ocomm_id"] = each_entry["ocomm_id"]
        each_entry_output["ocomm_name"] = each_entry["ocomm_name"]
        each_entry_output["ocomm_current_location"] = each_entry["ocomm_current_location"]
        each_entry_output["ocomm_current_shift_time"]["start_time"] = each_entry["start_datetime"].time().isoformat(timespec="minutes")
        each_entry_output["ocomm_current_shift_time"]["start_date"] = each_entry["start_datetime"].date().isoformat()
        each_entry_output["ocomm_current_shift_time"]["end_time"] = each_entry["end_datetime"].time().isoformat(timespec="minutes")
        each_entry_output["ocomm_current_shift_time"]["end_date"] = each_entry["end_datetime"].date().isoformat()
        each_entry_output["ocomm_contact"] = each_entry["ocomm_contact"]

        output["find_ocomm"].append(each_entry_output)
        output["_ocomm_count"] += 1

    return jsonify(output)
