from flask import current_app as app
from flask import jsonify, request
import flask_login

@flask_login.login_required
def _consumables_ID_update(id):
    """
    - updates columnes for consumables. if total qty updated, increase stock_qty accordingly
    - check that quota_per_group * number_of_groups <= total_qty
    - not allowed to update stock_qty
    - quota_per_group is updated before total_qty
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    body = request.json

    name = body.get("name", None)
    description = body.get("description", None)
    total_qty = body.get("total_qty", None)
    quota_per_group = body.get("quota_per_group", None)
    
    # update name and description
    attribute_list = [["name", name], ["description", description]]
    for each_attribute in attribute_list:
        if each_attribute[1]:
            query = "UPDATE consumable SET {0}='{1}' WHERE consumable_id='{2}'".format(each_attribute[0], each_attribute[1], id)
            with connection.cursor() as cursor:
                cursor.execute(query)
    
    if quota_per_group:
        query = "SELECT quota_per_group FROM consumable WHERE consumable_id='{0}'".format(id)
        with connection.cursor() as cursor:
            cursor.execute(query)
            old_quota_per_group = cursor.fetchall()[0]["quota_per_group"]
        
        if old_quota_per_group > quota_per_group:
            # check if any groups have already consumed more than new quota
            query = "SELECT `group`.name \
                FROM consumable_group \
                INNER JOIN `group` ON consumable_group.group_id=`group`.group_id \
                WHERE consumable_id='{0}' AND qty>{1}".format(id, quota_per_group)
            with connection.cursor() as cursor:
                cursor.execute(query)
                query_result = cursor.fetchall()
            
            if len(query_result) > 0:
                group_str = ""
                for each_consumable in query_result:
                    group_str += each_consumable["name"] + ", "
                group_str = group_str[:-2]

                return jsonify({"error": "groups {0} have consumed more than new quota".format(group_str)}), 400
        
        query = "UPDATE consumable SET quota_per_group={0} WHERE consumable_id='{1}'".format(quota_per_group, id)
        with connection.cursor() as cursor:
            cursor.execute(query)

    if total_qty:
        query = "SELECT total_qty FROM consumable WHERE consumable_id='{0}'".format(id)
        with connection.cursor() as cursor:
            cursor.execute(query)
            old_total_qty = cursor.fetchall()[0]["total_qty"]
    
        if old_total_qty > total_qty:
            # check if total_qty is more than amount already consumed
            query = "SELECT qty FROM consumable_group WHERE consumable_id='{0}'".format(id)
            with connection.cursor() as cursor:
                cursor.execute(query)
                query_result = cursor.fetchall()
            
            qty_alr_consumed = 0
            for each_qty in query_result:
                qty_alr_consumed += each_qty["qty"]
            
            if qty_alr_consumed > total_qty:
                return jsonify({"error": "quantity lesser than amount already consumed by groups"}), 400

        query = "UPDATE consumable SET total_qty={0}, stock_qty=stock_qty+{1} WHERE consumable_id='{2}'".format(total_qty, total_qty-old_total_qty, id)
        with connection.cursor() as cursor:
            cursor.execute(query)


    return jsonify({"success": "ok"}), 200
