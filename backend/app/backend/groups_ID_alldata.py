from flask import current_app as app
from flask import jsonify, request
import flask_login


# @flask_login.login_required
def _groups_ID_alldata(id):
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
