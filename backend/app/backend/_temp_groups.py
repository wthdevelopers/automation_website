from flask import current_app as app
from flask import jsonify, request


def groups_create():
    """
    Creates new groups
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    body = request.json

    name = body["name"]
    space = body["hacking_space"]

    query = "INSERT INTO `group` (name, space) VALUES ('{0}', '{1}')".format(name, space)
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.execute("SELECT @last_uuid;")
        new_group1_id = cursor.fetchall()[0]["@last_uuid"]

    output = {"group_id": new_group1_id}

    return jsonify(output), 200


def groups_get_basic_data():
    """
    Returns id, name, hacking space of all groups
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "SELECT \
            group_id as id, \
            name, \
            space as hacking_space \
        FROM `group`;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    # format output
    output = {"groups_get_all": [], "_groups_count": 0}

    for each_group in query_result:
        temp_group_details = {
            "id": each_group["id"], 
            "name": each_group["name"], 
            "hacking_space": each_group["hacking_space"]
        }
        
        output["groups_get_all"].append(temp_group_details)
        output["_groups_count"] += 1

    return jsonify(output), 200


def groups_get_all_data(id):
    """
    Returns all column data, including all categories it is in
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "SELECT \
            group_id as id, \
            name, \
            space as hacking_space \
        FROM `group` WHERE group_id='{0}';".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    query = "SELECT competition_category.name as category_name FROM `group` \
        INNER JOIN category_group ON `group`.group_id=category_group.group_id \
        INNER JOIN competition_category ON competition_category.category_id=category_group.category_id \
        WHERE `group`.group_id='{0}';".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        category_list = cursor.fetchall()


    # format output
    output = {"groups_ID_alldata": {
        "id": query_result[0]["id"],
        "name": query_result[0]["name"],
        "hacking_space": query_result[0]["hacking_space"],
        "competition_categories": [],
    }}

    for each_category in category_list:
        output["groups_ID_alldata"]["competition_categories"].append(each_category["category_name"])

    return jsonify(output), 200


def groups_change_single_col(hack_submitted):
    """
    Returns a tool from a specific group
    """
    #SNIP
    return "OK", 200


def groups_update_all_vals(id):
    """
    Updates all column values of group
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    body = request.json

    name = body["name"]
    space = body["hacking_space"]
    hack_submitted = body["hack_submitted"]

    query = "UPDATE `group` SET \
            name='{0}', \
            space='{1}', \
            hack_submitted='{2}' \
        WHERE group_id='{3}';".format(name, space, hack_submitted, id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    return "done", 200