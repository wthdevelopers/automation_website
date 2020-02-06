from flask import current_app as app
from flask import jsonify, request
import flask_login, pymysql


@flask_login.login_required
def _groups_create():
    """
    Creates new groups
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    body = request.json

    name = body.get("name", None)
    space = body.get("hacking_space", None)
    members = body.get("members", None)

    # check that name and space has values
    if not (name and space):
        return {"error": "name and/or hacking_space is not specified"}, 400

    # check datatype
    if not (isinstance(name, str) and isinstance(space, str)):
        return {"error": "name and/or space are not strings"}

    # check that name has not already been used
    query = "SELECT name FROM `group`;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        group_name_list = cursor.fetchall()
        cursor.close()

    for each_group_name in group_name_list:
        if each_group_name == name:
            return {"error": "group name already existed"}, 400

    # create and insert group
    query = "INSERT INTO `group` (name, space) VALUES ('{0}', '{1}')".format(pymysql.escape_string(name), pymysql.escape_string(space))
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.execute("SELECT @last_uuid;")
        new_group1_id = cursor.fetchall()[0]["@last_uuid"]
        cursor.close()

    # copied from /groups/ID/update_members
    if members and isinstance(members, list):
        # retrieve group_ids of all users in request body
        group_id_dict = {}
        
        for each_member_id in members:
            query = "SELECT group_id FROM user WHERE user_id='{0}'".format(pymysql.escape_string(each_member_id))
            with connection.cursor() as cursor:
                cursor.execute(query)
                group_id_dict[each_member_id] = cursor.fetchall()
                cursor.close()

        # check that all user_ids exist
        for each_member_id in group_id_dict:
            if not group_id_dict[each_member_id]:
                return {"error": "user_id: '{0}' in your request body does not exist in the user database".format(each_member_id)}, 400
        
        # check that group_id of all users are either null or the current group id
        for each_member_id in group_id_dict:
            each_member_group_id = group_id_dict[each_member_id][0]["group_id"]
            if each_member_group_id != None and each_member_group_id != new_group1_id:
                return {"error": "user_id: '{0}' in your request body belongs to another group".format(each_member_id)}, 400

        # allocate group_id to updated members
        for each_member_id in group_id_dict:
            if group_id_dict[each_member_id][0]["group_id"] == None:
                query = "UPDATE user SET group_id='{0}' WHERE user_id='{1}'".format(pymysql.escape_string(new_group1_id), pymysql.escape_string(each_member_id))
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    cursor.close()

    output = {"group_id": new_group1_id}

    return jsonify(output), 200
