from flask import Flask
from flask import render_template

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def start_page():
        return render_template('start_page.html')

    @app.route('/registration/')
    def registration():
        return render_template('registration_page.html')
    
    return app
