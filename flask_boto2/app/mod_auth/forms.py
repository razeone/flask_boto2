# wtf and RecaptchaField form
from flask_wtf import Form

from flask_wtf import RecaptchaField

# Import Form Elements such as textField and BooleanField
from wtforms import TextField
from wtforms import PasswordField

from wtforms import BooleanField

# Import form validators
from wtforms.validators import Required
from wtforms.validators import Email

from wtforms.validators import EqualTo



# Define login form (WTForms)

class LoginForm(Form):

    email = TextField('Email Address',
                      [Email(),
                       Required(message='Forgot Email Address?')
                       ]
                      )

    password = PasswordField('Password', [
        Required(message='Password Required')])
