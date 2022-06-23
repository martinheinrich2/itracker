import os
from app import create_app
from flask_migrate import Migrate
from flask import Flask

# app = Flask(__name__)
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
print("Current configuration: ", os.getenv('FLASK_CONFIG'))
# you need pip install python-dotenv to
app.config.from_prefixed_env()


if __name__ == '__main__':
    # On macOS change port or deactivate Sharing/AirPlay receiver

    app.run()
