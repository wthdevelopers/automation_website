from flask import current_app as app
from flask import jsonify, request


def participants_get_all_basicdata():
    """
    Returns basic information of all users
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    
    # retrieve group id
    participant_id = request.args.get("participant_id")
    query = "SELECT user_id as id, name, registered FROM user"
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    output = {"participants_all": [], "_participants_count": 0}
    for each_user in query_result:
        output["participants_all"].append({
            "id": each_user["id"],
            "name": each_user["name"],
            "registered": each_user["registered"]
        })
        output["_participants_count"] += 1

    return jsonify(output), 200


def participants_get_user_alldata(id):
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


def participants_deregister(id):
    """
    Deregisters an existing participant
    """
    query = "UPDATE user SET registered=0 WHERE user_id='{0}'".format(id)
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "done.", 200


def participants_register(id):
    """
    Registers an existing participant
    """
    query = "UPDATE user SET registered=1 WHERE user_id='{0}'".format(id)
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "done.", 200


def participants_is_already_grouped(id):
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


def participants_update_user(id):
    """
    Updates the particulars of an existing participant
    """
    body = request.json

    name = body["name"]
    contact_number = body["contact_number"]
    email = body["email"]
    group_id = body["group_id"]
    registered = body["registered"]
    DoB = body["DoB"]
    gender = body["gender"]
    nationality = body["nationality"]
    category_of_interest = body["category_of_interest"]
    technology_of_interest = body["technology_of_interest"]
    skills = body["skills"]
    organisation = body["organisation"]
    designation = body["designation"]
    dietary_pref = body["dietary_pref"]
    NoK_name = body["NoK_name"]
    NoK_relationship = body["NoK_relationship"]
    NoK_contact_number = body["NoK_contact_number"]

    query = "UPDATE user SET \
            name='{0}', \
            contact_number='{1}', \
            email='{2}', \
            group_id='{3}', \
            registered='{4}', \
            DoB='{5}', \
            gender='{6}', \
            nationality='{7}', \
            category_of_interest='{8}', \
            technology_of_interest='{9}', \
            skills='{10}', \
            organisation='{11}', \
            designation='{12}', \
            dietary_pref='{13}', \
            NoK_name='{14}', \
            NoK_relationship='{15}', \
            NoK_contact_number='{16}' \
        WHERE user_id='{17}';".format(
            name,
            contact_number,
            email,
            group_id,
            registered,
            DoB,
            gender,
            nationality,
            category_of_interest,
            technology_of_interest,
            skills,
            organisation,
            designation,
            dietary_pref,
            NoK_name,
            NoK_relationship,
            NoK_contact_number,
            id
        )
    connection = app.config["PYMYSQL_CONNECTION"]

    # submit query and retrieve values
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "done.", 200