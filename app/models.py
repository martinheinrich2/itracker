from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager


# Create User Model, use email to login instead of username
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    name = db.Column(db.String(64))
    user_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Add password hash
    password_hash = db.Column(db.String(128))

    # Create properties to set and verify password
    # Raise error if trying to read password

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Defining __repr__() method to control what to return for objects of users
    def __repr__(self):
        return '<Name %r>' % self.name


# The login_manager provides the user_loader callback, which is responsible for fetching
# the current user id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))