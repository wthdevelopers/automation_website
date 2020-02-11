from flask import current_app as app
from flask import jsonify, request
import flask_login, pymysql


@flask_login.login_required
def _groups_ID_alldata(id):
    """
    Returns all column data, including all categories it is in, and the name and id of users in the group
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "SELECT \
            group_id as id, \
            name, \
            space as hacking_space \
        FROM `group` WHERE group_id='{0}';".format(pymysql.escape_string(id))
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()
        cursor.close()

    query = "SELECT competition_category.name as category_name FROM `group` \
        INNER JOIN category_group ON `group`.group_id=category_group.group_id \
        INNER JOIN competition_category ON competition_category.category_id=category_group.category_id \
        WHERE `group`.group_id='{0}';".format(pymysql.escape_string(id))
    with connection.cursor() as cursor:
        cursor.execute(query)
        category_list = cursor.fetchall()
        cursor.close()

    query = "SELECT user_id, name FROM user WHERE group_id='{0}'".format(pymysql.escape_string(id))
    with connection.cursor() as cursor:
        cursor.execute(query)
        user_list = cursor.fetchall()
        cursor.close()

    # format output
    output = {"groups_ID_alldata": {
        "id": query_result[0]["id"],
        "name": query_result[0]["name"],
        "hacking_space": query_result[0]["hacking_space"],
        "competition_categories": [],
        "members": []
    }}

    for each_category in category_list:
        output["groups_ID_alldata"]["competition_categories"].append(each_category["category_name"])

    for each_user in user_list:
        output["groups_ID_alldata"]["members"].append({"name":each_user["name"], "user_id":each_user["user_id"]})

    return jsonify(output), 200
