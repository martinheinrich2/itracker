import unittest
from flask import current_app
from app import create_app, db


# setUp() and tearDown() methods run before and after each test by the testing
# Framework, methods beginning with test_ are executed as tests.
class BasicTestCase(unittest.TestCase):
    def setUp(self):
        # Creates environment for the test, tha is close to that of a running app,
        # creates app and activates its context.
        # Creates new database for testing from testing configuration
        # using SQLAlchemy's create_all() method.
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Database and applications are removed in this method
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
