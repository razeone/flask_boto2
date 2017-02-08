# Import the database obj from the main application module
# We will define this inside /app/__init__.py in the next sections.

import datetime
import re

from app import db
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin

from flask import session
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from app import db

import datetime


#
# We need groups for our account, if the account is grouped this means
# That we can control down to the group level on login user.id/group.id
# Found this on stack-overflow
#
groups = db.Table('groups',
                  db.Column('user_id',
                            db.Integer,
                            db.ForeignKey('user.id')
                            ),
                  db.Column('group_id',
                            db.Integer,
                            db.ForeignKey('group.id')
                            )
                  )

group_to_group = db.Table('group_to_group',
                          db.Column('parent_id',
                                    db.Integer,
                                    db.ForeignKey('group.id'),
                                    primary_key=True
                                    ),
                          db.Column('child_id',
                                    db.Integer,
                                    db.ForeignKey('group.id'),
                                    primary_key=True)
                          )


# Define a base model for other db tables to inherit
class Base(db.Model):

    __abstract__ = True
    # Auth Data role and status
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False,
                      unique=True)
    password = db.Column(db.String(192), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)
    created_at = db.Column(db.DateTime)
    is_authenticated = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    last_login = db.Column(db.DateTime, default=db.func.now())

    @declared_attr
    def role(cls):
        return db.relationship("Role")


# Define a User Model
class User(UserMixin, Base):
    __tablename__ = 'user'

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # New Instance: Instantion procedure
    def __init__(self, name, email, password, status, role_id):
        self.name = name
        self.email = email
        self.created_at = datetime.datetime.now()
        self.password = password
        self.status = status
        self.role_id = role_id
        self.order_by = User.name

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.name)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %r>' % (self.name)

#
# Effective class for grouping groups - this is apart of the StackOverflow snippet
#


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    kind = db.Column(db.String(32))
    allows = db.Column(db.Text)
    #users = db.relationship('user',
    #                        secondary=groups,
    #                        backref=db.backref('groups',
    #                                           lazy='dynamic',
    #                                           order_by=name
      #                                         )
     #                       )
    parents = db.relationship(
        'Group',
        secondary=group_to_group,
        primaryjoin=id == group_to_group.c.parent_id,
        secondaryjoin=id == group_to_group.c.child_id,
        backref="children",
        remote_side=[group_to_group.c.parent_id]
    )

    def __repr__(self):
        return self.name
