from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app
from flask import session
from flask import get_flashed_messages
from flask import jsonify
from flask import g
from flask import session
from flask import redirect
from flask import url_for

from flask_classy import FlaskView
from flask_classy import route

from flask_principal import identity_changed
from flask_principal import Identity

from jinja2 import TemplateNotFound

from app import app

from app.mod_auth.controllers import login

route_base = '/'
mod_base = Blueprint('base', __name__, url_prefix='/')


@mod_base.route('/', defaults={'page': 'login'})
def show(page):
    try:
        return render_template('%s.html' %
                               page,
                               authorization_url=login()
                               )
    except TemplateNotFound:
        return "Error: 404 Page Not Found", 404
