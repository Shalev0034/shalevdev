from re import S

from sqlalchemy.orm import relationship
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    schoolClass = db.Column(db.String(10))
    last_date=db.Column(db.String(20))

    tables = relationship("Table")
    majors=db.Column(db.String(150))

class Major(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    keywords = db.Column(db.String(1000))

class Table(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    table = db.Column(db.Text(4000))
    date = db.Column(db.String(50))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))