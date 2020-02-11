from flask import current_app as app
from flask import jsonify, request
import flask_login, pymysql


# @flask_login.login_required
def _participants_ID_deregister(id):
    """
    Deregisters an existing participant. Note that this removes the participant from any group he's registered in. If you register again you'll have to update the members of the group to add him back into the group.
    """
    query = "UPDATE user SET registered=0, group_id=NULL WHERE user_id='{0}'".format(pymysql.escape_string(id))
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.close()

    return {"success": "ok"}, 200

