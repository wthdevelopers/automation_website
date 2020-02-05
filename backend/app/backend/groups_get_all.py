from flask import current_app as app
from flask import jsonify, request
import flask_login


@flask_login.login_required
def _groups_get_all():
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
