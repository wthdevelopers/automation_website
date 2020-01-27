from flask import current_app as app
from flask import jsonify, request, session
import flask
import hashlib, flask_login


def _login():
    username = request.json['username']
    connection = app.config["PYMYSQL_CONNECTION"]

    query = "SELECT password FROM `credentials` WHERE username='{0}'".format(username)
    with connection.cursor() as cursor:
        cursor.execute(query)
        query_result = cursor.fetchall()

    hashed_salted_password = hashlib.sha256(bytes(request.json["password"] + app.config["PW_SALT"], "utf-8")).hexdigest()
    is_authenticated = hashed_salted_password == query_result[0]["password"]

    if is_authenticated:
        user = app.config["User"]()
        user.id = username
        output = flask_login.login_user(user)
        return jsonify({"success": "Logged in"}), 200

    return jsonify({"error": "Bad login"}), 400

def _logout():
    flask_login.logout_user()
    return jsonify({"success": "Logged out"}), 200

