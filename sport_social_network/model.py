from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.DateTime)
    male = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)

    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

    def __repr__(self):
        return f'<User {self.id} {self.email}>'
