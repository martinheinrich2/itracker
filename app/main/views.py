# Route applications are updated to be in the blueprint
import flask
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from . import main
from .forms import EditProfileForm, IssueForm, CommentForm, CreateIssueForm
from .. import db
from ..models import User, Role, Permission, Issue, Comment
from ..decorators import admin_required, permission_required
from sqlalchemy import or_

# Pagination default number of rows
ROWS_PER_PAGE = 10

# Main route to index.html
@main.route('/')
def index():
    return render_template('index.html', methods=['GET', 'POST'])


@main.route('/dashboard')
def dashboard():
    all_issues = Issue.query.count()
    open_issues = Issue.query.filter(Issue.status == 'Open').count()
    in_progress_issues = Issue.query.filter(Issue.status == 'In Progress').count()
    in_review_issues = Issue.query.filter(Issue.status == 'In Review').count()
    resolved_issues = Issue.query.filter(Issue.status == 'Resolved').count()
    closed_issues = Issue.query.filter(Issue.status == 'Closed').count()
    return render_template('dashboard.html', methods=['GET', 'POST'], open_issues=open_issues,
                           in_progress_issues=in_progress_issues,
                           in_review_issues=in_review_issues,
                           resolved_issues=resolved_issues,
                           closed_issues=closed_issues,
                           all_issues=all_issues)


# Display issues for users department
@main.route('/user-department-issues/<name>')
def user_department_issues(name):
    # Get user data
    user = User.query.filter_by(name=name).first_or_404()
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    filter_department_id = user.department_id
    # print(type(filter_department_id))
    issues = Issue.query.filter(Issue.department_id == filter_department_id).order_by(Issue.timestamp.desc()).paginate(
        page, per_page=ROWS_PER_PAGE, error_out=False)

    # Return all variables because jinja is unable to read them in this page.
    return render_template('department_user.html', user=user, issues=issues.items, issues_pages=issues.pages, page=page,
                           has_prev=issues.has_prev, has_next=issues.has_next, next_num=issues.next_num,
                           prev_num=issues.prev_num)


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
    form = CreateIssueForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        issue = Issue(title=form.title.data,
                      description=form.description.data,
                      status=form.status.data,
                      priority=form.priority.data,
                      department_id=form.department_id.data,
                      author=current_user._get_current_object())
        # Clear the Form
        form.title.data = ''
        form.description.data = ''
        form.status.data = ''
        form.priority.data = ''
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
    form = IssueForm(issue=issue)
    if form.validate_on_submit():
        issue.title = form.title.data
        issue.description = form.description.data
        issue.department_id = form.department_id.data
        issue.status = form.status.data
        issue.priority = form.priority.data
        db.session.add(issue)
        db.session.commit()
        flash('The Issue has been updated!')
        return redirect(url_for('.issue', id=issue.id))
    form.title.data = issue.title
    form.description.data = issue.description
    form.department_id.data = issue.department_id
    form.status.data = issue.status
    form.priority.data = issue.priority
    return render_template('edit_issue.html', form=form, issue=issue)


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
    issues = Issue.query.order_by(Issue.timestamp.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('issues.html', issues=issues)


# Test show all issues page wit Grid.js support
@main.route('/issues-list')
@login_required
def issues_list():
    return render_template('issues_list.html')


# Create API data
@main.route('/api/data')
def data():
    query = Issue.query

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(Issue.title.like(f'%{search}%'))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['title', 'id', 'author', 'timestamp', 'status', 'priority']:
                name = 'title'
            col = getattr(Issue, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [issue.to_dict() for issue in query],
        'total': total,
    }


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
