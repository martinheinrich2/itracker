from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from . import auth
from .. import db
from ..models import User, Role, Permission, Department
from ..decorators import admin_required
from .forms import LoginForm, ChangePasswordForm, RegistrationForm, ChangeUserAdminForm, AddDepartmentForm, EditDepartmentForm


# Pagination default value
ROWS_PER_PAGE = 10


# Add Department
@auth.route('/add_department', methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        flash('Department has been added.')
        return redirect(url_for('auth.list_departments'))
    else:
        flash('Sorry there was a problem adding the department. Please try again!')
    return render_template('auth/add_department.html', form=form)


# Delete Department
@auth.route('/delete-department/<int:id>')
@login_required
@admin_required
def delete_department(id):
    department_to_delete = Department.query.get_or_404(id)
    try:
        db.session.delete(department_to_delete)
        db.session.commit()
        flash('Department was deletet!')
        return redirect(url_for('.list_departments'))
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        message = f'There was a problem deleting the department! Error: {error}'
        flash(message)
        return redirect(url_for('.list_departments'))


# Edit Department
@auth.route('/edit-department/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_department(id):
    department = Department.query.get_or_404(id)
    if not current_user.can(Permission.ADMIN):
        abort(403)
    form = EditDepartmentForm(department=department)
    if form.validate_on_submit():
        department.name = form.name.data
        db.session.add(department)
        db.session.commit()
        flash('Department has been updated!')
        return redirect(url_for('auth.list_departments'))
    form.name.data = department.name
    return render_template('auth/edit_department.html', department=department, form=form)

# List all departments
@auth.route('/list_departments')
@login_required
@admin_required
def list_departments():
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    # Get all users from the database
    departments = Department.query.order_by('name').paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('auth/list_departments.html', departments=departments)


# Change user password
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
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


# Login to app
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            if not user.account_active:
                flash('Account Disabled')
            else:
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


# Logout from app
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    # return redirect(url_for('auth/login.html'))
    return redirect(url_for('auth.login'))


# Register new user
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


# List Users as Admin
@auth.route('/users')
@admin_required
def list_users():
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    # Get all users from the database
    users = User.query.order_by('name').paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('auth/list_users.html', users=users)


# Change User as Admin
@auth.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if not current_user.can(Permission.ADMIN):
        abort(403)
    form = ChangeUserAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.name = form.name.data
        user.job_description = form.job_description.data
        user.role_id = form.role_id.data
        user.department_id = form.department_id.data
        user.account_active = form.account_active.data
        db.session.add(user)
        db.session.commit()
        flash('User has been updated!')
        return redirect(url_for('auth.list_users'))
    form.email.data = user.email
    form.name.data = user.name
    form.job_description.data = user.job_description
    form.role_id.data = user.role_id
    form.department_id.data = user.department_id
    form.account_active.data = user.account_active
    return render_template('auth/edit_user.html', form=form, user=user)

