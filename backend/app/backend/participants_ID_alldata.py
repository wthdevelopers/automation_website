from flask import current_app as app
from flask import jsonify, request
import flask_login


# @flask_login.login_required
def _participants_ID_alldata(id):
    """
    Returns all information for one user
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    
    # retrieve group id
    participant_id = request.args.get("participant_id")
    query = "SELECT \
            user.user_id as id, \
            user.name, \
            user.contact_number, \
            user.email, \
            user.group_id, \
            user.registered, \
            user.DoB, \
            user.gender, \
            user.nationality, \
            user.organisation, \
            user.designation, \
            user.dietary_pref, \
            user.NoK_name, \
            user.NoK_relationship, \
            user.NoK_contact_number, \
            user.shirt_size, \
            user.previous_hackathons_attended, \
            user.bringing_utensils, \
            user.team_allocation_preference, \
            user.utensil_color \
        FROM user WHERE user_id='{0}'".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        user_data = cursor.fetchall()

    output = user_data[0]

    query = "SELECT competition_category.name as name \
        FROM user \
        INNER JOIN category_user \
            ON user.user_id=category_user.user_id \
        INNER JOIN competition_category \
            ON category_user.category_id=competition_category.category_id \
        WHERE \
            user.user_id='{0}'".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()
    
    output["category_of_interest"] = []
    for each_category in query_result:
        output["category_of_interest"].append(each_category["name"])
    
    query = "SELECT _user_preference_technology_of_interest.name as name \
        FROM user \
        INNER JOIN _user_preference_technology_of_interest_user \
            ON user.user_id=_user_preference_technology_of_interest_user.user_id \
        INNER JOIN _user_preference_technology_of_interest \
            ON _user_preference_technology_of_interest_user.technology_of_interest_id=_user_preference_technology_of_interest.technology_of_interest_id \
        WHERE \
            user.user_id='{0}'".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()
    
    output["technology_of_interest"] = []
    for each_category in query_result:
        output["technology_of_interest"].append(each_category["name"])

    query = "SELECT _user_preference_skills.name as skill, _user_preference_skills_user.other_skills as other_skills \
        FROM user \
        INNER JOIN _user_preference_skills_user \
            ON user.user_id=_user_preference_skills_user.user_id \
        LEFT JOIN _user_preference_skills \
            ON _user_preference_skills_user.skills_id=_user_preference_skills.skills_id \
        WHERE \
            user.user_id='{0}'".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    output["skills"] = {"default_skills": [], "other_skills": []}
    for each_skill in query_result:
        if each_skill["skill"]:
            output["skills"]["default_skills"].append(each_skill["skill"])
        elif each_skill["other_skills"]:
            output["skills"]["other_skills"].append(each_skill["other_skills"])
        else:
            pass
    
    query = "SELECT _user_preference_utensil_name.name as utensil_name \
        FROM user \
        INNER JOIN _user_preference_utensil_name_user \
            ON user.user_id=_user_preference_utensil_name_user.user_id \
        INNER JOIN _user_preference_utensil_name \
            ON _user_preference_utensil_name_user.utensil_name_id=_user_preference_utensil_name.utensil_name_id \
        WHERE \
            user.user_id='{0}'".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    output["utensil_name"] = []
    for each_utensil in query_result:
        output["utensil_name"].append(each_utensil["utensil_name"])

    query = "SELECT _user_preference_workshops.name as workshop_name, _user_preference_workshops_user.level_of_preference as workshop_level_of_preference \
        FROM user \
            INNER JOIN _user_preference_workshops_user \
                ON user.user_id=_user_preference_workshops_user.user_id \
            INNER JOIN _user_preference_workshops \
                ON _user_preference_workshops_user.workshops_id=_user_preference_workshops.workshops_id \
            WHERE \
                user.user_id='{0}'".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    output["workshop"] = []
    for each_workshop in query_result:
        output["workshop"].append({"name": each_workshop["workshop_name"], "level_of_preference": each_workshop["workshop_level_of_preference"]})

    output = {"participants_ID_alldata": output}

    return jsonify(output), 200
