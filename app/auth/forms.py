from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


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


class ChangeUserForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(1, 64), Regexp('[A-Za-z]', 0,
                                                                                 'Usernames must have only letters.')])
    role_id = SelectField('Role:', choices=[('1', 'User'),
                                        ('2', 'Moderator'),
                                        ('3', 'Administrator')], coerce=int)
    submit = SubmitField('Submit')