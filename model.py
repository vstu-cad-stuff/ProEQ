from __init__ import db
from enum import Enum


class UserRole(Enum):
    USER = 0
    ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    role = db.Column(db.Integer)

    def __init__(self, username, password, role=UserRole.USER):
        self.username = username
        self.password = password
        self.role = role.value

    def __repr__(self):
        return "<User('{}', '{}', {})>".format(self.username, self.password, self.role)
