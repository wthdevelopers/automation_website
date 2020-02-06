from flask import current_app as app
from flask import jsonify, request
import flask_login, pymysql


@flask_login.login_required
def _tools_get_all():
    """
    Retrieves details of each tool and the name of the lastest user that loaned it
    """

    connection = app.config["PYMYSQL_CONNECTION"]

    query = "SELECT \
            tool.tool_id as tool_id, \
            tool.loaned as loaned_status, \
            tool.name as name, \
            tool.description as description, \
            `group`.name as group_name, \
            loan.loan_datetime as loan_datetime \
        FROM tool \
        LEFT JOIN \
            loan ON tool.latest_loan=loan.loan_id \
        LEFT JOIN \
            `group` ON loan.loan_to_group_id=`group`.group_id;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()
        cursor.close()

    output = {"tools_get_all": [], "_tools_count": 0}

    for i in query_result:
        temp_tool_details = {
            "tool_id": i["tool_id"],
            "loaned_status": i["loaned_status"],
            "name": i["name"],
            "description": i.get("description", None),
            "group_name": i.get("group_name", None),
            "loan_datetime": i.get("loan_datetime", None)
        }

        output["tools_get_all"].append(temp_tool_details)
        output["_tools_count"] += 1

    return jsonify(output), 200
