from flask import current_app as app
from flask import jsonify, request, session
import flask_login, pymysql


@flask_login.login_required
def _participants_get_all():
    """
    Returns basic information of all users
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    
    # retrieve group id
    participant_id = request.args.get("participant_id")
    query = "SELECT user_id as id, name, registered, given_cash FROM user"
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()
        cursor.close()

    output = {"participants_all": [], "_participants_count": 0}
    for each_user in query_result:
        output["participants_all"].append({
            "id": each_user["id"],
            "name": each_user["name"],
            "registered": each_user["registered"],
            "given_cash": each_user["given_cash"]
        })
        output["_participants_count"] += 1

    return jsonify(output), 200
