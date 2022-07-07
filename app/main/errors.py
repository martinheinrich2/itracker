# Error handler in main blueprint, app_errorhandler decorator installs
# application-wide handlers. It is used for all requests even outside the
# blueprint

from flask import render_template
from . import main


@main.app_errorhandler(403)
def forbidden_page(e):
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
