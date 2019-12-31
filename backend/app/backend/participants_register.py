from flask import current_app as app
from flask import jsonify, request


def _participants_register():
    """
    Registers an existing participant
    """
    participant_id = request.args.get("participant_id")
    query = "UPDATE user SET participating=1 WHERE user_id='{0}'".format(participant_id)
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "done."

