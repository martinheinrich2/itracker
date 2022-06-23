# Main blueprint creation to implement app functionality

from flask import Blueprint

# Create a blueprint with name main and tell Flask the blueprint has its own template and static directories.
main = Blueprint('main', __name__, static_folder='static', template_folder='templates')

from . import views, errors

