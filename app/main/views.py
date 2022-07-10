# Route applications are updated to be in the blueprint
import flask
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from . import main
from .forms import EditProfileForm, IssueForm, CommentForm
from .. import db
from ..models import User, Role, Permission, Issue, Comment
from ..decorators import admin_required, permission_required

# Pagination default number of rows
ROWS_PER_PAGE = 10

# Main route to index.html
@main.route('/')
def index():
    return render_template('index.html', methods=['GET', 'POST'])


# Display user name
@main.route('/user/<name>')
def user(name):
    # Grab all issues for user by name
    user = User.query.filter_by(name=name).first_or_404()
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)

    issues = user.issues.order_by(Issue.timestamp.desc()).paginate(
                                            page, per_page=ROWS_PER_PAGE, error_out=False)
    # Return all variables because jinja is unable to read them in this page.
    return render_template('user.html', user=user, issues=issues.items, issues_pages=issues.pages, page=page,
                           has_prev=issues.has_prev, has_next=issues.has_next, next_num=issues.next_num,
                           prev_num=issues.prev_num)


# Edit User Profile page
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form  = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.job_description = form.job_description.data
        # get the actual object and not the proxy from current_user.id, to avoid confusion
        # with SQLAlchemy
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', name=current_user.name))
    form.name.data = current_user.name
    form.job_description.data = current_user.job_description
    return render_template(('edit_profile.html'), form=form)


# Add new issue
@main.route('/add-issue', methods=['GET', 'POST'])
@login_required
def add_issue():
    form = IssueForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        issue = Issue(title=form.title.data,
                      description=form.description.data,
                      assigned_to=form.assigned_to.data,
                      status=form.status.data,
                      author=current_user._get_current_object())
        # Clear the Form
        form.title.data = ''
        form.description.data = ''
        form.assigned_to.data = ''
        db.session.add(issue)
        db.session.commit()

        # Return Message
        flash('Issue has been submitted!')
    return render_template('add_issue.html', form=form)


# Edit issue
@main.route('/edit-issue/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_issue(id):
    issue = Issue.query.get_or_404(id)
    if not current_user.can(Permission.MODERATE) and not current_user.can(Permission.ADMIN):
        abort(403)
    form = IssueForm()
    if form.validate_on_submit():
        issue.title=form.title.data
        issue.description=form.description.data
        issue.assigned_to=form.assigned_to.data
        issue.status=form.status.data
        db.session.add(issue)
        db.session.commit()
        flash('The Issue has been updated!')
        return redirect(url_for('.issue', id=issue.id))
    form.title.data = issue.title
    form.description.data = issue.description
    form.assigned_to.data = issue.assigned_to
    form.status.data = issue.status
    return render_template('edit_issue.html', form=form)


# Edit comment
@main.route('/edit-comment/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_comment(id):
    comment = Comment.query.get_or_404(id)
    if not current_user.can(Permission.ADMIN):
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.body = form.body.data
        db.session.add(comment)
        db.session.commit()
        flash('The Comment has been updated!')
        return redirect(url_for('.issues'))
    form.body.data = comment.body
    return render_template('edit_comment.html', form=form)


# Delete Comment
@main.route('/delete-comment/<int:id>')
@login_required
@admin_required
def delete_comment(id):
    comment_to_delete = Comment.query.get_or_404(id)
    try:
        db.session.delete(comment_to_delete)
        db.session.commit()
        flash('Comment was deleted!')
        return redirect(url_for('.issues'))
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        message = f'There was a problem deleting the comment! Error: {error}'
        flash(message)
        return redirect(url_for('.issues'))



# Show all Issues Page
@main.route('/issues')
@login_required
def issues():
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    # Grab all issues from the database, use SQLAlchemy pagination
    # issues = Issue.query.order_by(Issue.timestamp.desc())
    issues = Issue.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('issues.html', issues=issues)


# Show individual Issue
@login_required
@main.route('/issue/<int:id>', methods=['GET', 'POST'])
def issue(id):
    # Grab individual post from the database
    issue = Issue.query.get_or_404(id)
    # Add Comment
    form = CommentForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          issue_id=issue.id,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been saved.')
        return redirect(url_for('.issue', id=issue.id))

    comments = issue.comments.order_by(Comment.timestamp.desc()).all()
    return render_template('issue.html', issue=issue, form=form,
                           comments=comments)
