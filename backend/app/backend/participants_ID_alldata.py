from flask import current_app as app
from flask import jsonify, request
import flask_login


@flask_login.login_required
def _participants_ID_alldata(id):
    """
    Returns all information for one user
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    
    # retrieve group id
    participant_id = request.args.get("participant_id")
    query = "SELECT \
            user_id as id, \
            name, \
            contact_number, \
            email, \
            group_id, \
            registered, \
            DoB, \
            gender, \
            nationality, \
            category_of_interest, \
            technology_of_interest, \
            skills, \
            organisation, \
            designation, \
            dietary_pref, \
            NoK_name, \
            NoK_relationship, \
            NoK_contact_number \
        FROM user WHERE user_id='{0}'".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    output = {"participants_ID_alldata": [query_result[0]]}

    return jsonify(output), 200
