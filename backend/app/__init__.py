from flask import Flask
import os, sys
import pymysql.cursors

# import logic for each endpoint as blueprints
dirname = os.path.dirname(__file__)
sys.path.append(dirname)
import backend 


def create_app():
    # initialize the core application
    app = Flask(__name__, instance_relative_config=False)

    # add config values
    flask_env = os.environ["FLASK_ENV"]
    if flask_env == "local":
        app.config.from_object('config.LocalConfig')
    elif flask_env == "devVM":
        app.config.from_object('config.DevVMConfig')

    # initialise mysql connections and attach it to global app config object
    PyMySQL = pymysql.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USERNAME"],
        password=app.config["MYSQL_PASSWORD"],
        db=app.config["MYSQL_DATABASE"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    app.config.from_mapping(
                PYMYSQL_CONNECTION = PyMySQL
            )

    with app.app_context():
        # Register Blueprints
        app.register_blueprint(backend.module)

        return app
