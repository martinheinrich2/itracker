from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64), Regexp('[A-Za-z]', 0,
                                                                                 'Usernames must have only letters.')])
    job_description = StringField('Job Description', validators=[Length(0, 64)])
    submit = SubmitField('Submit')
