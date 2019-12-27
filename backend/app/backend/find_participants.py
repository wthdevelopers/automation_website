from flask import current_app as app
from flask import jsonify, request

def _find_participants():
    """
    Returns information of participants and their allocated groups
    """
    query_participant_name = request.args.get("participant_name")
    query = "SELECT \
            user.uid as participant_id, \
            user.name as participant_name, \
            user.contact_number as participant_contact, \
            grp.gname as participant_team_name, \
            grp.space as participant_team_location \
        FROM user INNER JOIN grp ON user.gid=grp.gid \
        WHERE user.name LIKE '%{0}%'".format(query_participant_name)
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    # parse query output into formatted output
    output = {"find_participants": [], "_participants_count": 0}
    for each_entry in query_result:
        each_entry_output = {}
        each_entry_output["participant_id"] = each_entry["participant_id"]
        each_entry_output["participant_name"] = each_entry["participant_name"]
        each_entry_output["participant_contact"] = each_entry["participant_contact"]
        each_entry_output["participant_team_name"] = each_entry["participant_team_name"]
        each_entry_output["participant_team_location"] = each_entry["participant_team_location"]

        output["find_participants"].append(each_entry_output)
        output["_participants_count"] += 1

    return jsonify(output)
