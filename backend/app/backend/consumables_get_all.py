from flask import current_app as app
from flask import jsonify, request
import flask_login

@flask_login.login_required
def _consumables_get_all():
    """
    Returns id, name, remaining count, quota per group
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    # retrieve group id
    query = "SELECT \
            consumable_id as id, \
            name, \
            total_qty-stock_qty as remaining_count, \
            quota_per_group \
        FROM consumable;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    # format output
    output = {"consumables_get_all": [], "_consumables_count": 0}

    for each_consumable in query_result:
        temp_consumable_details = {
            "id": each_consumable["id"], 
            "name": each_consumable["name"], 
            "remaining_count": each_consumable["remaining_count"], 
            "quota_per_group": each_consumable["quota_per_group"]
        }
        
        output["consumables_get_all"].append(temp_consumable_details)
        output["_consumables_count"] += 1

    return jsonify(output), 200
