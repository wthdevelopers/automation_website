from flask import Flask
import os, sys
dirname = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(dirname, "modules"))
import test

# Globally accessible libraries


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins

    with app.app_context():
        # Register Blueprints
        app.register_blueprint(test.module)
        # app.register_blueprint(admin.admin_bp)

        return app
