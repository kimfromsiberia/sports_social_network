from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String, index=True)
    last_name = db.Column(db.String, index=True)
    date_of_birth = db.Column(db.DateTime)
    male = db.Column(db.String)
    contry = db.Column(db.String, index=True)
    city = db.Column(db.String, index=True)

    def __repr__(self):
        return f'<User {self.id} {self.email}>'
