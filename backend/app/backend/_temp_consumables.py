from flask import current_app as app
from flask import jsonify, request


def _consumables_ID_take_ID_count(group_id, consumable_id, count):
    """
    Notifies that the group would be consuming a certain amount of consumables
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "CREATE PROCEDURE UpdateConsumedQty() \
        BEGIN \
            SELECT 'HONK HONK HONK'; \
            \
            DECLARE `remaining_count`, `quota_per_group`, `qty_already_consumed` INT DEFAULT 0; \
            \
            SELECT total_qty-stock_qty \
            INTO remaining_count \
            FROM consumable WHERE consumable_id='{0}'; \
            \
            IF remaining_count-{2} >= 0 THEN \
                SELECT quota_per_group \
                INTO quota_per_group \
                FROM consumable WHERE consumable_id='{0}'; \
                \
                SELECT qty \
                INTO qty_already_consumed\
                FROM consumable_group \
                WHERE consumable_id='{0}' AND group_id='{1}'; \
                \
                IF quota_per_group-qty_already_consumed-{2} >= 0 THEN \
                    UPDATE consumable_group \
                    SET qty=qty_already_consumed+{2} \
                    WHERE consumable_id='{0}' AND group_id='{1}'; \
                    \
                    UPDATE consumable \
                    SET stock_qty=stock_qty+{2} \
                    WHERE consumable_id='{0}'; \
                    \
                    SELECT 'OK'; \
                ELSE \
                    SELECT 'Quantity requested exceeds quota of group'; \
                END IF; \
            ELSE \
                SELECT 'Insufficient consumables to meet request'; \
            END IF; \
        END;".format(consumable_id, group_id, count)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    print("query_result: {0}".format(query_result))

    return jsonify({"query_result": query_result}), 200


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
