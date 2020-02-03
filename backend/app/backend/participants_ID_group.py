from flask import current_app as app
from flask import jsonify, request
import flask_login


# @flask_login.login_required
def _participants_ID_group(id):
    """
    Returns whether the participant exist, and whether it belongs in an existing group already
    """
    connection = app.config["PYMYSQL_CONNECTION"]

    query = "SELECT group_id FROM user WHERE user_id='{0}'".format(id)
    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    output = {"user_exist": 0,"group_id": None}
    print("query_result: {0}".format(query_result))
    if query_result != ():
        output["user_exist"] = 1
        if query_result != [{}]:
            output["group_id"] = query_result[0]["group_id"]

    return jsonify(output), 200


