from flask import current_app as app
from flask import jsonify, request
import flask_login


@flask_login.login_required
def _participants_ID_update(id):
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

