import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Permission



# app = Flask(__name__)
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
print("Current configuration: ", os.getenv('FLASK_CONFIG'))
# you need pip install python-dotenv to
# app.config.from_prefixed_env()


# Use the shell_context_processor decorator to configure the shell command to automatically
# import the database and tables. Returns a dictionary including the database
# instance and models.
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role,
                Permission=Permission)


# Add Unit tests
@app.cli.command()
def test():
    import unittest
    # Finds and returns all test modules in the directory and subdirectories.
    tests = unittest.TestLoader().discover('tests')
    # Displays results as text
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    # On macOS change port or deactivate Sharing/AirPlay receiver

    app.run()
