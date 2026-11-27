from flask import Flask

from config import Config


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes.main import main
    from app.routes.assistant import assistant

    app.register_blueprint(main)
    app.register_blueprint(assistant)

    return app
