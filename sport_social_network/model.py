from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.DateTime)
    male = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)

    def __repr__(self):
        return f'<User {self.id} {self.email}>'
