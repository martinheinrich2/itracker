# Route applications are updated to be in the blueprint

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm
from .. import db
from ..models import User, Role, Permission


@main.route('/')
def index():
    return render_template('index.html', methods=['GET', 'POST'])


@main.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form  = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.job_description = form.job_description.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', name=current_user.name))
    form.name.data = current_user.name
    form.job_description.data = current_user.job_description
    return render_template(('edit_profile.html'), form=form)
