from flask import Flask
import os, sys
import sqlalchemy as db

# import modules
dirname = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(dirname, "modules"))
import test
from config import Config


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
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins

    with app.app_context():
        # load config file
        app.config.from_pyfile(CONFIG_DIR, silent=False)

        # Register Blueprints
        app.register_blueprint(test.module)
        # app.register_blueprint(admin.admin_bp)

        return app
