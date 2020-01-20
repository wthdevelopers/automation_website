from flask import current_app as app
from flask import jsonify, request


def loans_get_all_data():
    """
    Retrieves details of each tool and the name of the lastest user that loaned it
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "SELECT \
            tool.name as tool_name, \
            tool.tool_id as tool_id, \
            tool.loaned as loaned, \
            `group`.name as on_loan_to \
        FROM tool \
        LEFT JOIN \
            loan ON tool.latest_loan=loan.loan_id \
        LEFT JOIN \
            `group` ON loan.loan_to_group_id=`group`.group_id;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    output = {"loans_get_all": [], "_tools_count": 0}

    for i in query_result:
        temp_tool_details = {}
        temp_tool_details["tool_name"] = i["tool_name"]
        temp_tool_details["tool_id"] = i["tool_id"]
        temp_tool_details["loaned"] = i["loaned"]
        temp_tool_details["on_loan_to"] = i["on_loan_to"]

        output["loans_get_all"].append(temp_tool_details)
        output["_tools_count"] += 1

    return jsonify(output), 200


def loans_lend_out_item(group_id, tool_id):
    """
    Loans a tool to a specific group
    Check
    1. If tool has been returned

    Does
    1. Create new loan row
    2. Update status and latest_loan of tool
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    # check that tool has not already been loaned
    query = "SELECT loaned FROM tool WHERE tool_id='{0}'".format(tool_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    if query_result[0]["loaned"] == 1:
        return jsonify({"error": "tool has already been loaned out"}), 400

    # ELSE
    # insert new loan entry
    current_datetime = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    query = "INSERT INTO loan (tool_id, loan_to_group_id, loan_datetime) VALUES ('{0}', '{1}', '{2}')".format(tool_id, group_id, current_datetime)
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.execute("SELECT @last_uuid;")
        new_loan_id = cursor.fetchall()[0]["@last_uuid"]
    
    # update into existing tool row
    query = "UPDATE tool SET latest_loan='{0}', loaned=1 WHERE tool_id='{1}'".format(new_loan_id, tool_id)
    with connection.cursor() as cursor:
        cursor.execute(query)


    return "OK", 200


def loans_return_item(tool_id):
    """
    Returns a tool from a specific group
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "UPDATE tool SET loaned='0' WHERE tool_id='{0}'".format(tool_id)
    with connection.cursor() as cursor:
        cursor.execute(query)

    return "OK", 200