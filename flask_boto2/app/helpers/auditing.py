from flask_login import current_user
import sys


class Audit(dict):

    def __init__(self, action=None, user=None, method=None):
        super(Audit, self).__init__()
        self['action'] = action
        self['audit'] = True
        self['method'] = method or sys._getframe(1).f_code.co_name
        self['user'] = user or current_user.name
