from flask import current_app as app
from flask import jsonify, request
import flask_login


@flask_login.login_required
def _consumables_ID_take_ID_count(group_id, consumable_id, count):
    """
    Allow a group to consume a certain amount of consumables
    """

    connection = app.config["PYMYSQL_CONNECTION"]
    count = int(count)

    # checks if there is enough stock to meet request
    query = "SELECT stock_qty-{0} AS remaining_count \
            FROM consumable WHERE consumable_id='{1}';".format(count, consumable_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    if query_result[0]["remaining_count"] < 0:
        return jsonify({"error": "Insufficient consumables to meet request"}), 400

    # checks if group did not exceed its quota for consumable
    query = "SELECT qty AS qty_left \
        FROM consumable_group \
        WHERE group_id='{0}' AND consumable_id='{1}'".format(group_id, consumable_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    print("query_result: {0}".format(query_result))

    if query_result[0]["qty_left"] - count < 0:
        return jsonify({"error": "Quantity requested exceeds quota of group"}), 400

    # updates records and approve the distribution of consumables
    query = "UPDATE consumable_group \
        SET qty=qty-{0} \
        WHERE consumable_id='{1}' AND group_id='{2}';".format(count, consumable_id, group_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
    
    query = "UPDATE consumable \
        SET stock_qty=stock_qty-{0} \
        WHERE consumable_id='{1}';".format(count, consumable_id)
    with connection.cursor() as cursor:
        cursor.execute(query)

    # query = "CREATE PROCEDURE UpdateConsumedQty() \
    #     BEGIN \
    #         SELECT 'HONK HONK HONK'; \
    #         \
    #         DECLARE `remaining_count` INT DEFAULT 0; \
    #         DELCARE `quota_per_group` INT DEFAULT 0; \
    #         DECLARE `qty_already_consumed` INT DEFAULT 0; \
    #         \
    #         SELECT total_qty-stock_qty \
    #         INTO remaining_count \
    #         FROM consumable WHERE consumable_id='{0}'; \
    #         \
    #         IF remaining_count-{2} >= 0 THEN \
    #             SELECT quota_per_group \
    #             INTO quota_per_group \
    #             FROM consumable WHERE consumable_id='{0}'; \
    #             \
    #             SELECT qty \
    #             INTO qty_already_consumed\
    #             FROM consumable_group \
    #             WHERE consumable_id='{0}' AND group_id='{1}'; \
    #             \
    #             IF quota_per_group-qty_already_consumed-{2} >= 0 THEN \
    #                 UPDATE consumable_group \
    #                 SET qty=qty_already_consumed+{2} \
    #                 WHERE consumable_id='{0}' AND group_id='{1}'; \
    #                 \
    #                 UPDATE consumable \
    #                 SET stock_qty=stock_qty+{2} \
    #                 WHERE consumable_id='{0}'; \
    #                 \
    #                 SELECT 'OK'; \
    #             ELSE \
    #                 SELECT 'Quantity requested exceeds quota of group'; \
    #             END IF; \
    #         ELSE \
    #             SELECT 'Insufficient consumables to meet request'; \
    #         END IF; \
    #     END;".format(consumable_id, group_id, count)
    # with connection.cursor() as cursor:
    #     cursor.execute(query)
    #     query_result = cursor.fetchall()

    return "OK", 200
