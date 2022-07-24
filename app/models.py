from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


# Class for comments
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'))


# Class for departmens
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='department', lazy='dynamic')
    issues = db.relationship('Issue', backref='department', lazy='dynamic')

    @staticmethod
    def insert_departments():
        departments = ['Administration', 'Building Services', 'Housekeeping', 'IT', 'Reception', 'Social Work',
                       'Vehicles', 'Unknown']
        default_department = 'Unknown'
        for d in departments:
            department = Department.query.filter_by(name=d).first()
            if department is None:
                department = Department(name=d)
            department.default = (department.name == default_department)
            db.session.add(department)
        db.session.commit()

    # Defining __repr__() method to control what to return for objects of users
    def __repr__(self):
        return '<Name %r>' % self.name


# Class for issues
class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='issue', lazy='dynamic')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    status = db.Column(db.String(64))
    priority = db.Column(db.String(64))


# Class for permissions of user/roles
class Permission:
    READ = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


# Class of user roles
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # Column has an index to speed up searches in the roles table
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # Changes standard None permission set by SQLAlchemy in db to 0
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.READ, Permission.WRITE, Permission.COMMENT],
            'Moderator': [Permission.READ, Permission.WRITE, Permission.COMMENT, Permission.MODERATE],
            'Administrator': [Permission.READ, Permission.WRITE, Permission.COMMENT, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        # Uses the bitwise and operator & to check if a combined permission value
        # includes given the given basic permissions
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


# Create User Model, use email to login instead of username
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    job_description = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    user_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Add password hash
    password_hash = db.Column(db.String(128))
    issues = db.relationship('Issue', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    account_active = db.Column(db.Boolean, default=True)

    # Assigns the role Administrator if the email matches a config value,
    # otherwise set default role to User.
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ITRACKER_ADMIN']:
                print("Assigning Admin Privileges")
                print(self.email)
                self.role = Role.query.filter_by(name='Administrator').first()
                print(self.role)
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
            # if self.department is None:
            #    self.department = Department.query.filter_by(default=True).first()

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

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def is_moderator(self):
        return self.can(Permission.MODERATE)

    # Defining __repr__() method to control what to return for objects of users
    def __repr__(self):
        return '<Name %r>' % self.name


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


# The login_manager provides the user_loader callback, which is responsible for fetching
# the current user id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
