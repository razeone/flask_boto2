from flask import request
from flask import abort

from app import db

from app.mod_auth.models import User
from app.mod_auth.role_controller import RoleController


import datetime


USERS_GROUP_NAME = '_user'
ADMIN_GROUP_NAME = '_admin'


class UserController(User):
    """
    Used to handle database transactions and data validation.
    """

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.role = RoleController.get_role_by_name(USERS_GROUP_NAME)
        self.name = raw_data['name']
        self.email = raw_data['email']
        # For Google login we're storing remote id as password
        self.password = raw_data['id']
        self.errors = ""

        if raw_data['verified_email']:
                    self.status = 1

        if self.role is None:
            self.role = RoleController(USERS_GROUP_NAME).create_role()

        self.user = User(
            name=self.name,
            email=self.email,
            password=self.password,
            status=self.status,
            role_id=self.role.id)

    def __is_valid(self):
        try:
            if self.raw_data['hd'] != 'domain.name':
                return False, "Error: Only gem google users are allowed"
            else:
                return True, "Data is valid"
        except Exception as e:
            return False, "Error: Cannot find organization name"

    def create_admin_user(self):
        validation = self.__is_valid()

        if validation[0]:
            try:
                role = RoleController.get_role_by_name('_admin')

                if role is None:
                    role = RoleController.create_role('_admin')

                self.user.role_id = role.id
                db.session.add(self)
                db.session.commit()
                return self

            except Exception as e:
                return e, 500

        else:
            self.errors = validation[1]

    def create_user(self):
        validation = self.__is_valid()

        if validation[0]:
            try:
                db.session.add(self)
                db.session.commit()
                return self

            except Exception as e:
                return e, 500

        else:
            self.errors = validation[1]

    @staticmethod
    def get_user_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        user_instance = User.query.get(user_id)
        return user_instance

    def validate_user(*args, **kwargs):
        credentials = request.headers.get('Authorization', None)
        if credentials:
            name, passwd = credentials.split(":")
            try:
                if auth.alternate(name, passwd):
                    u = user.User.query.filter_by(name=name).first()
                    return u
            except Exception, e:
                print e
            try:
                if auth.authenticate(name, passwd):
                    return user.User.query.filter_by(name=name).first()
            except:
                abort(401)
        return user.AnonymousUser()
