from flask import Flask
import os, sys
import pymysql.cursors, flask_login
from flask_login import LoginManager

# import logic for each endpoint as blueprints
dirname = os.path.dirname(__file__)
sys.path.append(dirname)
import backend 

def create_app():
    # initialize the core application
    app = Flask(__name__, instance_relative_config=False)

    # add config values
    flask_env = os.environ.get("FLASK_ENV", "RemoteTest")
    if flask_env == "Production":
        app.config.from_object('config.Production')
    elif flask_env == "RemoteTest":
        app.config.from_object('config.RemoteTest')

    # initialise mysql connections and attach it to global app config object
    PyMySQL = pymysql.connect(
        host=app.config["HOST"],
        user=app.config["USER"],
        password=app.config["PW"],
        db=app.config["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    PyMySQL.autocommit(True)
    app.config.from_mapping(
                PYMYSQL_CONNECTION = PyMySQL
            )

    # initialize plugins
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    class User(flask_login.UserMixin):
        pass
    app.config["User"] = User

    @login_manager.user_loader
    def user_loader(username):
        # retrieve all usernames
        from flask import current_app as app
        connection = app.config["PYMYSQL_CONNECTION"]
        query = "SELECT username FROM `credentials`;"
        with connection.cursor() as cursor:
            cursor.execute(query)
            query_result = cursor.fetchall()

        # check if username exists
        username_not_in_db_state = True
        for i in query_result:
            if i["username"] == username:
                username_not_in_db_state = False

        if username_not_in_db_state:
            # print("!!! user_loader used - username_not_in_db_state", file=sys.stderr)
            return

        user = User()
        user.id = username

        return user


    @login_manager.request_loader
    def request_loader(request):
        # retrieve all usernames
        from flask import current_app as app
        connection = app.config["PYMYSQL_CONNECTION"]
        query = "SELECT username FROM `credentials`;"
        with connection.cursor() as cursor:
            cursor.execute(query)
            query_result = cursor.fetchall()

        username = request.form.get('username')

        # check if username exists
        username_not_in_db_state = True
        for i in query_result:
            if i["username"] == username:
                username_in_db_state = False

        if username_not_in_db_state:
            return

        user = User()
        user.id = username

        # retrieve hash password
        query = "SELECT password FROM `credentials` WHERE username='{0}'".format(username)
        with connection.cursor() as cursor:
            cursor.execute(query)
            query_result = cursor.fetchall()

        # DO NOT ever store passwords in plaintext and always compare password
        # hashes using constant-time comparison!
        import hashlib
        hashed_salted_password = hashlib.sha256(bytes(request.form["password"] + app.config["PW_SALT"], "utf-8")).hexdigset()
        user.is_authenticated = hashed_salted_password == query_result[0]["password"]

        return user
    
    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return 'Unauthorized'

    with app.app_context():
        # Register Blueprints
        app.register_blueprint(backend.module)

        return app
