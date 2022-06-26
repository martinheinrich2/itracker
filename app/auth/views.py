from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, ChangePasswordForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # login_user() function records user logged in and optional
            # remember_me boolean value, setting a long-term cookie if true
            login_user(user)
            # Get the original URL requested by the user
            next = request.args.get('next')
            # get the original URL to prevent malicious user from redirecting users to another site
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            flash('Logged in successfully.')
            return redirect(next)
        flash('Invalid Name or Password!')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    # return redirect(url_for('auth/login.html'))
    return redirect(url_for('auth.login'))


@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('/auth/change_password.html', form=form)