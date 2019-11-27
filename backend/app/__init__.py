from flask import Flask
import os, sys
import sqlalchemy as db

# import modules
dirname = os.path.dirname(__file__)
sys.path.append(dirname)
import backend 
from config import localConfig as Config


CONFIG_DIR = "config.py"

# Globally accessible libraries
sqlengine = db.create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(
    Config.MYSQL_USER, 
    Config.MYSQL_PASSWORD, 
    Config.HOST, 
    Config.DATABASE_NAME
))
sqlengine.connect()

def create_app():
    # initialize the core application
    app = Flask(__name__, instance_relative_config=False)

    # add config values
    flask_env = os.environ["FLASK_ENV"]
    if flask_env == "local":
        app.config.from_object('config.localConfig')

    with app.app_context():
        # load config file

        # Register Blueprints
        app.register_blueprint(backend.module)

        return app
