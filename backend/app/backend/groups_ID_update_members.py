from flask import current_app as app
from flask import jsonify, request
import flask_login


@flask_login.login_required
def _groups_ID_update_members(id):
    """
    Updates the team members in a group. If group no longer has any team members, group is deleted. Check that user inserted does not belong in another group.
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    members = request.json.get("members", None)

    print("members: {0}".format(members))

    if not members:
        return {"error": "request body does not include key 'members' with values (a list with the ID of users)"}, 400

    # retrieve group_ids of all users in request body
    group_id_dict = {}
    
    for each_member_id in members:
        query = "SELECT group_id FROM user WHERE user_id='{0}'".format(each_member_id)
        with connection.cursor() as cursor:
            cursor.execute(query)
            group_id_dict[each_member_id] = cursor.fetchall()

    print("group_id_dict: {0}".format(group_id_dict))

    # check that all user_ids exist
    for each_member_id in group_id_dict:
        if not group_id_dict[each_member_id]:
            return {"error": "user_id: '{0}' in your request body does not exist in the user database".format(each_member_id)}, 400
    
    # check that group_id of all users are either null or the current group id
    for each_member_id in group_id_dict:
        each_member_group_id = group_id_dict[each_member_id][0]["group_id"]
        if each_member_group_id != None and each_member_group_id != id:
            return {"error": "user_id: '{0}' in your request body belongs to another group".format(each_member_id)}, 400
    
    # remove members that are not one of the updated members
    query = "UPDATE user SET group_id=NULL WHERE group_id='{0}'".format(id)
    for each_member_id in group_id_dict:
        query += " AND user_id!='{0}'".format(each_member_id)
    query += ";"
    print("query: {0}".format(query))
    with connection.cursor() as cursor:
        cursor.execute(query)

    # allocate group_id to updated members
    for each_member_id in group_id_dict:
        if group_id_dict[each_member_id][0]["group_id"] == None:
            query = "UPDATE user SET group_id='{0}' WHERE user_id='{1}'".format(id, each_member_id)
            with connection.cursor() as cursor:
                cursor.execute(query)

    return jsonify({"success": "ok"}), 200
