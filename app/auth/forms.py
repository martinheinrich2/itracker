from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Role, Department


class AddDepartmentForm(FlaskForm):
    name = StringField('Department', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Add Department')


class EditDepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Edit Department')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                             message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    # Only allow letters as username
    name = StringField('Name', validators=[DataRequired(), Length(1, 64), Regexp('[A-Za-z]', 0,
                                                                                 'Usernames must have only letters.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                             message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    # Check if email is in database
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')


class ChangeUserAdminForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    name = StringField('Name:', validators=[DataRequired(), Length(1, 64), Regexp('[A-Za-z]', 0,
                                                                                  'Usernames must have only letters.')])
    # role_id = SelectField('Role:', choices=[('1', 'User'),
                                       # ('2', 'Moderator'),
                                       # ('3', 'Administrator')], coerce=int)
    # SelectField takes a list of tuples
    role_id = SelectField('Role', coerce=int)
    department_id = SelectField('Department', coerce=int)
    submit = SubmitField('Submit')

    # Get roles from database model
    def __init__(self, user, *args, **kwargs):
        super(ChangeUserAdminForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [(role_id.id, role_id.name)
                                for role_id in Role.query.order_by(Role.name).all()]
        self.department_id.choices = [(department_id.id, department_id.name)
                                      for department_id in Department.query.order_by(Department.name).all()]
        self.user = user

    # Check if email is in database
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
