from flask import current_app as app
from flask import jsonify, request


def _groups_create():
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
