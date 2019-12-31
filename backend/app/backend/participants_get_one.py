from flask import current_app as app
from flask import jsonify, request


def _participants_get_one():
    """
    Returns event information of all events where the starting date is today
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    
    # retrieve group id
    participant_id = request.args.get("particiapant_id")
    query = "SELECT group_id FROM user WHERE user_id='{0}'".format(participant_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        group_id = cursor.fetchall()
        print("group_id: {0}\n\n".format(group_id))

    # retrieve user and team member info
    query = "SELECT \
            user.user_id as participant_id, \
            user.name as participant_name, \
            group.space as participant_team_location, \
            user.contact_number as participant_contact, \
            group.name as participant_team_name, \
        FROM user \
        INNER JOIN \
            `group` ON group.group_id='{0}' AND user.group_id=group.group_id;".format(group_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()
        print("query_result: {0}\n\n".format(query_result))

    return "hi"
