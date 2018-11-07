from flask import Flask
from instance.config import app_config
from .api.v2 import v2

def create_app(config_name):
    """app configuration"""
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(v2, url_prefix="/api/v2")

    return app