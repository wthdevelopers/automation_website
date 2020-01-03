from flask import current_app as app
from flask import jsonify, request


def _participants_get_one():
    """
    Returns information of the user and their group mates
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    
    # retrieve group id
    participant_id = request.args.get("participant_id")
    query = "SELECT group_id FROM user WHERE user_id='{0}'".format(participant_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        group_id = cursor.fetchall()[0]["group_id"]

    # retrieve user and team member info
    query = "SELECT \
            user.user_id as participant_id, \
            user.name as participant_name, \
            group.space as participant_team_location, \
            user.contact_number as participant_contact, \
            group.name as participant_team_name \
        FROM `user` \
        INNER JOIN \
            `group` ON group.group_id='{0}' AND user.group_id=group.group_id;".format(group_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    # format output
    output = {"participant_details":{"participant_details":{}, "participant_team_name": None, "team_member_details": [], "_team_member_number": 0}}
    for i in query_result:
        print("i[\"participant_id\"]: {0}, participant_id: {1}".format(i["participant_id"], participant_id))
        if i["participant_id"] == participant_id:
            output["participant_details"]["participant_details"]["participant_id"] = i["participant_id"]
            output["participant_details"]["participant_details"]["participant_name"] = i["participant_name"]
            output["participant_details"]["participant_details"]["participant_team_location"] = i["participant_team_location"]
            output["participant_details"]["participant_details"]["participant_contact"] = i["participant_contact"]
            output["participant_details"]["participant_team_name"] = i["participant_team_name"]
        else:
            team_member_details = {}
            team_member_details["participant_id"] = i["participant_id"]
            team_member_details["participant_name"] = i["participant_name"]
            team_member_details["participant_team_location"] = i["participant_team_location"]
            team_member_details["participant_contact"] = i["participant_contact"]

            output["participant_details"]["team_member_details"].append(team_member_details)
            output["participant_details"]["_team_member_number"] += 1

    return jsonify(output)
