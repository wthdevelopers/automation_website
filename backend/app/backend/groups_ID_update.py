from flask import current_app as app
from flask import jsonify, request
import flask_login


@flask_login.login_required
def _groups_ID_update(id):
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
