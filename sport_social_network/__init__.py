from flask import Flask
from flask import render_template

sport_app = Flask(__name__)

@sport_app.route('/')
def start_page():
    return render_template('start_page.html')

@sport_app.route('/registration/')
def registration():
    return render_template('registration_page.html')

if __name__ == '__main__':
    sport_app.run(debug=True)