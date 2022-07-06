# Route applications are updated to be in the blueprint

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, IssueForm, CommentForm
from .. import db
from ..models import User, Role, Permission, Issue, Comment
from ..decorators import admin_required, permission_required


# Main route to index.html
@main.route('/')
def index():
    return render_template('index.html', methods=['GET', 'POST'])


# Display user name
@main.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    issues = user.issues.order_by(Issue.timestamp.desc()).all()
    return render_template('user.html', user=user, issues=issues)


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


# Show all Issues Page
@main.route('/issues')
@login_required
def issues():
    # Grab all issues from the database
    issues = Issue.query.order_by(Issue.timestamp)
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
