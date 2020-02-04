from flask import current_app as app
from flask import jsonify, request
import flask_login, os, json, pymysql

# for checking user input with schema
filedir = os.path.dirname(__file__)
jsondir = os.path.join(filedir, '../../../insert_userdata/preference_categories_schema.json')

with open(jsondir, "r") as read_file:
    schema = json.loads(read_file.read())

@flask_login.login_required
def _groups_ID_update(id):
    """
    Updates all column values of group
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    body = request.json

    name = body.get("name", None)
    hacking_space = body.get("hacking_space", None)
    category = body.get("category", None)

    if name or hacking_space:
        attributes_list = [["name", name], ["space", hacking_space]]
        query = "UPDATE `group` SET "
        for each_attribute in attributes_list:
            if each_attribute[1]:
                query += "{0}='{1}', ".format(each_attribute[0], each_attribute[1])
        query = query[:-2] + " WHERE group_id='{0}'".format(id)
        print("query: {0}".format(query))
        with connection.cursor() as cursor:
            cursor.execute(query)
    
    if category:
        for each_category in category:
            if each_category not in schema["category"]:
                return jsonify({"error": "Value of key category did not obey schema"})
        
        # remove old values
        query = "DELETE FROM category_group WHERE group_id='{0}';".format(id)
        with connection.cursor() as cursor:
            cursor.execute(query)

        # retrieve ids of the values that we'll be inserting
        category_ids = []
        for each_category in category:
            query = "SELECT category_id FROM competition_category WHERE name='{0}';".format(pymysql.escape_string(each_category))
            with connection.cursor() as cursor:
                cursor.execute(query)
                category_ids.append(cursor.fetchall()[0]["category_id"])
        
        # insert new values
        for each_category_index in range(len(category)):
            query = "INSERT INTO category_group (category_id, group_id) VALUES ('{0}', '{1}');".format(category_ids[each_category_index], id)
            with connection.cursor() as cursor:
                cursor.execute(query)


    return jsonify({"success": "ok"}), 200
