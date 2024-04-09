from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    user_type = db.Column(db.String)
    sport_object = db.relationship('SportObject', uselist=False, back_populates='user')
    person = db.relationship('Person', uselist=False, back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id} {self.email}>'


class Person(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.DateTime)
    male = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)
    user = db.relationship('User', uselist=False, back_populates='person')

    def __repr__(self):
        return f'<Person {self.id} {self.user.email}>'


class SportObject(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    user = db.relationship('User', uselist=False, back_populates='sport_object')

    def __repr__(self):
        return f'<Sport object {self.id} {self.user.email}>'
