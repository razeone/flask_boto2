# Flask Deps
# Import PW and encrypt helper tools
# Import db obj from main app module
# Import Module forms
# Import Module models(User)
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import LoginManager

from flask_oauth2_login import GoogleLogin

from app import app

from app.mod_auth.models import User

from app.mod_auth.user_controller import UserController

import base64

# class AuthView(FlaskView):
# Define the blueprint auth set its url prefix app.url/auth
# You can expand on this
route_base = '/'
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
login_manager = LoginManager()
login_manager.init_app(app)
google_login = GoogleLogin(app)


@login_manager.user_loader
def load_user(user_id):
    return UserController.get_user_by_id(user_id)


@login_manager.header_loader
def load_user_from_header(header_val):
    header_val = header_val.replace('Bearer ', '', 1)
    try:
        header_val = base64.b64decode(header_val)
    except TypeError:
        pass
    return User.query.filter_by(api_key=header_val).first()


@app.route("/login")
def login():
    return render_template('auth/login.html',
                           authorization_url=google_login.authorization_url())


@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route("/user/<user_id>", methods=['GET'])
@login_required
def user_profile(user_id):
    user = UserController.get_user_by_id(user_id)
    return render_template('auth/profile.html', user=user)


@google_login.login_success
def login_success(token, profile):

    user = UserController.get_user_by_email(profile['email'])

    if user is None:
        user_controller = UserController(profile)
        try:
            user = user_controller.create_user()
            if user_controller.errors != "":
                flash(user_controller.errors)
                return redirect('/login')
        except Exception as e:
            return e

    login_user(user)
    return render_template(
        'index.html',
        token=token,
        profile=profile,
        user=user)


@google_login.login_failure
def login_failure(e):
    return redirect('/login')
