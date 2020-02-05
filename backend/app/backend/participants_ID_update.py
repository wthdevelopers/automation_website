from flask import current_app as app
from flask import jsonify, request
import flask_login, json, os, pymysql


# for checking user input with schema
filedir = os.path.dirname(__file__)
jsondir = os.path.join(filedir, '../../../insert_userdata/preference_categories_schema.json')

default_or_other_values = ["dietary_pref", "NoK_relationship"]  # list of keys with values that are either the default provided values, or could be a custom value

with open(jsondir, "r") as read_file:
    schema = json.loads(read_file.read())


@flask_login.login_required
def _participants_ID_update(id):
    """
    Updates the particulars of an existing participant
    """
    body =  request.json
    connection = app.config["PYMYSQL_CONNECTION"]


    ### update any relevant column values for user
    attributes_to_update = []
    attributes_to_update.append(["name", body.get("name", None)])
    attributes_to_update.append(["contact_number", body.get("contact_number", None)])
    attributes_to_update.append(["email", body.get("email", None)])
    attributes_to_update.append(["DoB", body.get("DoB", None)])
    attributes_to_update.append(["gender", body.get("gender", None)])
    attributes_to_update.append(["nationality", body.get("nationality", None)])
    attributes_to_update.append(["organisation", body.get("organisation", None)])
    attributes_to_update.append(["designation", body.get("designation", None)])
    attributes_to_update.append(["dietary_pref", body.get("dietary_pref", None)])
    attributes_to_update.append(["NoK_name", body.get("NoK_name", None)])
    attributes_to_update.append(["NoK_relationship", body.get("NoK_relationship", None)])
    attributes_to_update.append(["NoK_contact_number", body.get("NoK_contact_number", None)])
    attributes_to_update.append(["shirt_size", body.get("shirt_size", None)])
    attributes_to_update.append(["previous_hackathons_attended", body.get("previous_hackathons_attended", None)])
    attributes_to_update.append(["bringing_utensils", body.get("bringing_utensils", None)])
    attributes_to_update.append(["team_allocation_preference", body.get("team_allocation_preference", None)])
    attributes_to_update.append(["utensil_color", body.get("utensil_color", None)])

    query = None
    for each_attribute in attributes_to_update:
        if each_attribute[1]:
            # assign appropriate value for insertion, and exempt the value from checks if it has a non-default value
            value_to_insert = each_attribute[1]
            check_default_values = True
            if each_attribute[0] in default_or_other_values:
                if each_attribute[1]["default"]:
                    value_to_insert = each_attribute[1]["default"]
                elif each_attribute[1]["other"]:
                    value_to_insert = each_attribute[1]["other"]
                    check_default_values = False
                else:
                    return jsonify({"error": "Both values from 'default' and 'other' from user attribute {0} are null".format(each_attribute[0])}), 400

            # return error if value does not match the schema of its key (if the schema exists)
            if schema.get(each_attribute[0], None) and check_default_values:
                if value_to_insert not in schema[each_attribute[0]]:
                    print("value_to_insert: {0}; schema[each_attribute[0]]: {1}".format(value_to_insert, schema[each_attribute[0]]))
                    return jsonify({"error": "Value of key {0} did not obey schema".format(each_attribute[0])}), 400

            # append update statement to query, escape any invalid characters in user input
            if not query:
                query = "UPDATE user SET "  # if query was still None
            if isinstance(value_to_insert, str):
                query += "{0}='{1}', ".format(each_attribute[0], pymysql.escape_string(value_to_insert))
                # query += "{0}='{1}', ".format(each_attribute[0], value_to_insert)
            elif isinstance(value_to_insert, int):
                query += "{0}={1}, ".format(each_attribute[0], value_to_insert)
            else:
                return jsonify({"error": "Type of input is neither string nor integer"}), 400

    # return error if none of the predefined keys are found in request body
    if not query:
        return jsonify({"error": "No input found in request body"}), 400

    query = query[:-2] + " WHERE user_id='{0}';".format(id)  # remove commas, and touch up the update query
    with connection.cursor() as cursor:
        cursor.execute(query)


    ### update other user attributes that require the update of other tables
    attributes_to_update = []
    attributes_to_update.append(["technology_of_interest", body.get("technology_of_interest", None)])
    attributes_to_update.append(["utensil_name", body.get("utensil_name", None)])

    for each_attribute in attributes_to_update:
        if each_attribute[1]:
            # check input validity
            for each_attribute_value in each_attribute[1]:
                if each_attribute_value not in schema[each_attribute[0]]:
                    return jsonify({"error": "Value of key {0} did not obey schema".format(each_attribute[0])}), 400
            
            # remove old values
            query = "DELETE FROM _user_preference_{0}_user WHERE user_id='{1}';".format(each_attribute[0], id)
            with connection.cursor() as cursor:
                cursor.execute(query)

            # retrieve ids of the values that we'll be inserting
            attribute_ids = []
            for each_attribute_value in each_attribute[1]:
                query = "SELECT {0}_id FROM _user_preference_{0} WHERE name='{1}';".format(each_attribute[0], pymysql.escape_string(each_attribute_value))
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    attribute_ids.append(cursor.fetchall()[0]["{0}_id".format(each_attribute[0])])
            
            # insert new values
            for each_attribute_value_index in range(len(each_attribute[1])):
                query = "INSERT INTO _user_preference_{0}_user ({0}_id, user_id) VALUES ('{1}', '{2}');".format(each_attribute[0], attribute_ids[each_attribute_value_index], id)
                with connection.cursor() as cursor:
                    cursor.execute(query)
    
    ### update category of interest attribute (its db table naming convention is not similar to that of the other user_preference attributes)
    category_of_interest = body.get("category_of_interest", None)
    if category_of_interest:
        # check input validity
        for each_category in category_of_interest:
            if each_category not in schema["category"]:
                return jsonify({"error": "Value of key {0} did not obey schema".format(each_attribute[0])}), 400
        
        # remove old values
        query = "DELETE FROM category_user WHERE user_id='{0}';".format(id)
        with connection.cursor() as cursor:
            cursor.execute(query)

        # retrieve ids of the values that we'll be inserting
        category_ids = []
        for each_category in category_of_interest:
            query = "SELECT category_id FROM competition_category WHERE name='{0}';".format(pymysql.escape_string(each_category))
            with connection.cursor() as cursor:
                cursor.execute(query)
                category_ids.append(cursor.fetchall()[0]["category_id"])
        
        # insert new values
        for each_category_index in range(len(category_of_interest)):
            query = "INSERT INTO category_user (category_id, user_id) VALUES ('{0}', '{1}');".format(category_ids[each_category_index], id)
            with connection.cursor() as cursor:
                cursor.execute(query)

    ### update skills attribute
    skills = body.get("skills", None)

    if skills:
        # check input validity
        for each_default_skill in skills["default"]:
            if each_default_skill not in schema["skills"]:
                return jsonify({"error": "Value of key skills did not obey schema"}), 400

        # remove old values
        query = "DELETE FROM _user_preference_skills_user WHERE user_id='{0}';".format(id)
        with connection.cursor() as cursor:
            cursor.execute(query)
        
        # retrieve ids of the default values that we'll be inserting
        attribute_ids = []
        for each_default_skill in skills["default"]:
            query = "SELECT skills_id FROM _user_preference_skills WHERE name='{0}';".format(each_default_skill)
            with connection.cursor() as cursor:
                cursor.execute(query)
                attribute_ids.append(cursor.fetchall()[0]["skills_id"])
        
        # insert new default values
        for each_default_skill_index in range(len(skills["default"])):
            query = "INSERT INTO _user_preference_skills_user (skills_id, other_skills, user_id) VALUES ('{0}', null, '{1}');".format(attribute_ids[each_default_skill_index], id)
            with connection.cursor() as cursor:
                cursor.execute(query)
        
        # insert custom values
        for each_custom_skill in skills["other"]:
            query = "INSERT INTO _user_preference_skills_user (skills_id, other_skills, user_id) VALUES (null, '{0}', '{1}');".format(each_custom_skill, id)
            with connection.cursor() as cursor:
                cursor.execute(query)

    
    ### update workshop attribute
    workshop = body.get("workshop", None)

    if workshop:
        # check input validity
        for each_workshop in workshop:
            if each_workshop["name"] not in schema["workshop"]:
                return jsonify({"error": "Value of key workshop did not obey schema"}), 400
        
        # remove old values
        query = "DELETE FROM _user_preference_workshops_user WHERE user_id='{0}';".format(id)
        with connection.cursor() as cursor:
            cursor.execute(query)
        
        # retrieve ids of the default values that we'll be inserting
        attribute_ids = []
        for each_workshop in workshop:
            query = "SELECT workshops_id FROM _user_preference_workshops WHERE name='{0}';".format(each_workshop["name"])
            with connection.cursor() as cursor:
                cursor.execute(query)
                attribute_ids.append(cursor.fetchall()[0]["workshops_id"])
        
        # insert new default values
        for each_workshop_index in range(len(workshop)):
            query = "INSERT INTO _user_preference_workshops_user (workshops_id, user_id, level_of_preference) VALUES ('{0}', '{1}', {2});".format(attribute_ids[each_workshop_index], id, workshop[each_workshop_index]["level_of_preference"])
            with connection.cursor() as cursor:
                cursor.execute(query)

    return jsonify({"success": "done"}), 200
