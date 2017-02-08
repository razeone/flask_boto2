from flask import Flask
from flask import render_template

from flask_sqlalchemy import SQLAlchemy
from werkzeug.debug import DebuggedApplication

import logging
import gevent
import gevent.monkey
import os

gevent.monkey.patch_all(subprocess=True)

CONFIG_ENVIRONMENT = {
    'production': 'config.ProductionConfig',
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig'
}

# define the wsgi app obj and static url path

app = Flask(__name__,
            instance_relative_config=True,
            static_folder='./static',
            static_url_path='/static'
            )

log_format = (
    '\n' +
    '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
    '%(message)s\n' +
    '-' * 80
)
logging.basicConfig(format=log_format)

if app.config.get('UWSGI_DEBUG', False):
    print('!!! WARNING !!!  Enabling UWSGI Debug Module...DEV ONLY!')
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

# Config
GEM_ENVIRONMENT = CONFIG_ENVIRONMENT[os.environ['GEM_ENVIRONMENT']]
app.config.from_object(GEM_ENVIRONMENT)

# Define db obj which is imported by
# modules and ctrlers
db = SQLAlchemy(app)

# Sample HTTP error handling


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module for using its bprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_base.controllers import mod_base as base_module
from app.mod_aws.controllers import mod_aws as aws_module

# Register blueprint(s)
app.register_blueprint(base_module)
app.register_blueprint(auth_module)
app.register_blueprint(aws_module)
# app.register_blueprint(new_module)
# ..

# Build the db:
# This creates the db file using sqlalchemy!
db.create_all()


class InvalidApiUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
