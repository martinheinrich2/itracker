# Route applications are updated to be in the blueprint

from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html', methods=['GET', 'POST'])

