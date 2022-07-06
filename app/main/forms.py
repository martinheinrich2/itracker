from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, AnyOf
from wtforms import ValidationError
from ..models import Role, User


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64), Regexp('[A-Za-z]', 0,
                                                                                 'Usernames must have only letters.')])
    job_description = StringField('Job Description', validators=[Length(0, 64)])
    submit = SubmitField('Submit')


class IssueForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired('Please enter title')])
    description = TextAreaField('Description', validators=[DataRequired('Please enter description.')])
    # assigned_to = StringField('Assigned to', validators=[DataRequired('Please enter department.')])
    assigned_to = SelectField('Assigned to:', choices=[('Electrician', 'Electrician'),
                                                       ('Housekeeping', 'Housekeeping'),
                                                       ('IT', 'IT'),
                                                       ('Janitor', 'Janitor'),
                                                       ('Plumber', 'Plumber')])
    status = BooleanField('Status Open/Closed', default=True, validators=[AnyOf([True, False])])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired('Please enter comment.')])
    submit = SubmitField('Submit')
