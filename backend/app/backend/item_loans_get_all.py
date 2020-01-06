from flask import current_app as app
from flask import jsonify, request


def _item_loans_get_all():
    """
    Retrieves details of each tool and the name of the lastest user that loaned it
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    # retrieve group id
    query = "SELECT \
            tool.name as tool_name, \
            tool.tool_id as tool_id, \
            tool.status as status, \
            user.name as on_loan_to \
        FROM tool \
        LEFT JOIN \
            loan ON tool.latest_loan=loan.loan_id \
        LEFT JOIN \
            user ON loan.loan_to_user_id=user.user_id;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    # format output
    output = {"item_loans_get_all": [], "_item_count": 0}

    for i in query_result:
        temp_tool_details = {}
        temp_tool_details["tool_name"] = i["tool_name"]
        temp_tool_details["tool_id"] = i["tool_id"]
        temp_tool_details["status"] = i["status"]
        temp_tool_details["on_loan_to"] = i["on_loan_to"]

        output["item_loans_get_all"].append(temp_tool_details)
        output["_item_count"] += 1

    return jsonify(output)
