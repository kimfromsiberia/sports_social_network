from flask import Flask
from flask import render_template

from sport_social_network.model import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route('/')
    def start_page():
        return render_template('start_page.html')

    @app.route('/registration/')
    def registration():
        return render_template('registration_page.html')
    
    return app
