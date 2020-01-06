from flask import current_app as app
from flask import jsonify

def _upcoming_events():
    """
    Returns event information of all events where the starting date is today
    """
    # initialize queries and connections
    query = "SELECT \
            event_id as event_id, \
            name as event_name, \
            start_datetime, \
            end_datetime, \
            place as event_location \
        FROM event \
        WHERE CURDATE() BETWEEN DATE(start_datetime) AND DATE(end_datetime);"
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    # parse query output into formatted output
    output = {"functions_upcoming_events":[], "_upcoming_events_count":0}
    for each_event in query_result:
        each_event_output = {"event_time": {}}
        each_event_output["event_id"] = each_event["event_id"]
        each_event_output["event_name"] = each_event["event_name"]
        each_event_output["event_time"]["start_time"] = each_event["start_datetime"].time().isoformat(timespec="minutes")
        each_event_output["event_time"]["start_date"] = each_event["start_datetime"].date().isoformat()
        each_event_output["event_time"]["end_time"] = each_event["end_datetime"].time().isoformat(timespec="minutes")
        each_event_output["event_time"]["end_date"] = each_event["end_datetime"].date().isoformat()
        each_event_output["event_location"] = each_event["event_location"]

        output["functions_upcoming_events"].append(each_event_output)
        output["_upcoming_events_count"] += 1

    # print("output: {0}\n\n".format(output))

    return jsonify(output)
