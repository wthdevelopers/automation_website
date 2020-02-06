from flask import current_app as app
from flask import jsonify, request
import flask_login, datetime, pymysql


@flask_login.login_required
def _loans_ID_loan_ID(group_id, tool_id):
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
    query = "SELECT loaned FROM tool WHERE tool_id='{0}'".format(pymysql.escape_string(tool_id))
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()
        cursor.close()

    if query_result[0]["loaned"] == 1:
        return jsonify({"error": "tool has already been loaned out"}), 400

    # ELSE
    # insert new loan entry
    current_datetime = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    query = "INSERT INTO loan (tool_id, loan_to_group_id, loan_datetime) VALUES ('{0}', '{1}', '{2}')".format(pymysql.escape_string(tool_id), pymysql.escape_string(group_id), current_datetime)
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.execute("SELECT @last_uuid;")
        new_loan_id = cursor.fetchall()[0]["@last_uuid"]
        cursor.close()
    
    # update into existing tool row
    query = "UPDATE tool SET latest_loan='{0}', loaned=1 WHERE tool_id='{1}'".format(new_loan_id, pymysql.escape_string(tool_id))
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.close()


    return {"success": "ok"}, 200
