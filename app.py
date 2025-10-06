from flask import Flask
import os
from src.controllers import analysis_bp
from src.config import config
from src.utils import setup_logging


def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    setup_logging(app.config.get('LOG_LEVEL', 'INFO'))
    app.register_blueprint(analysis_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=app.config.get('DEBUG', True),
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 8082)
    )
