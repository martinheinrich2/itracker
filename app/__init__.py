# Application package constructor
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


# Create uninitialized instances because there is no application instance to initialize with
db = SQLAlchemy()
login_manager = LoginManager()

# Prefix is required because the login route is inside a blueprint
login_manager.login_view = 'auth.login'


# Allows directly import configuration settings in classes from config.py using the from_object() method
# in the app.config configuration object. Configuration is selected by name from config directory.
# init_app() completes the initialization of extensions
# missing routes and custom error page handlers are in app/main/__init__.py
def create_app(config_name):
    app = Flask(__name__)
    # you need pip install python-dotenv to
    app.config.from_prefixed_env()
    app.config.from_object(config[config_name])
    print(f"In __init__.py config is: {config_name}")

    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Register the defined blueprint from "/app/main/__init__.py" in our Flask app.
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # Register the defined blueprint from "/app/auth/__init__.py" in our Flask app.
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
