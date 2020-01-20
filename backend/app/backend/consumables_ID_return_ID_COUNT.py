from flask import current_app as app
from flask import jsonify, request


def _consumables_ID_return_ID_COUNT(group_id, consumable_id, count):
    """
    Allow a group to return a certain amount of consumables
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    count = int(count)

    # checks if returning stock exceeds total stock of consumables
    query = "SELECT total_qty-stock_qty-{0} AS remaining_count \
            FROM consumable WHERE consumable_id='{1}';".format(count, consumable_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    if query_result[0]["remaining_count"] < 0:
        return jsonify({"error": "Resulting quantity is more than original amount of consumables"}), 400

    # checks if returning stock gives the group more qty to begin in the first place
    query = "SELECT \
            consumable.quota_per_group AS quota_per_group, \
            consumable_group.qty AS qty_left \
        FROM consumable \
        INNER JOIN consumable_group ON consumable.consumable_id=consumable_group.consumable_id \
        WHERE consumable_group.group_id='{0}'".format(group_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    print("query_result: {0}".format(query_result))

    if query_result[0]["quota_per_group"] - query_result[0]["qty_left"] - count < 0:
        return jsonify({"error": "Resulting quantity requested exceeds original quota of group"}), 400

    # updates records and approve the distribution of consumables
    query = "UPDATE consumable_group \
        SET qty=qty+{0} \
        WHERE consumable_id='{1}' AND group_id='{2}';".format(count, consumable_id, group_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
    
    query = "UPDATE consumable \
        SET stock_qty=stock_qty+{0} \
        WHERE consumable_id='{1}';".format(count, consumable_id)
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "OK", 200
