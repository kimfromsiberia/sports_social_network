from flask import flash, Flask, redirect, request, url_for, render_template
from flask_login import current_user, LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash

from sport_social_network.model import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'start_page'

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    
    @app.route('/', methods=['GET', 'POST'])
    def start_page():
        if current_user.is_authenticated:
            return 'Страница находится в разработке.'
        if request.method == 'POST':
            email = request.form['email']
            if email:
                user = User.query.filter(User.email == email).first()
                if user:
                    if user.check_password(request.form['password']):
                        login_user(user)
                        return 'Страница находится в разработке.'
                    else:
                        flash('Неверный пароль')
                        return redirect(url_for('start_page'))
                else:
                    flash('Пользователя с такой почтой не существует')
                    return redirect(url_for('start_page'))
            else:
                flash('Введите почту')
                return redirect(url_for('start_page'))
        return render_template('start_page.html')


    @app.route('/registration/', methods=['GET', 'POST'])
    def registration():
        if request.method == 'POST':
            email = request.form['email']
            if email:
                user = User.query.filter(User.email == email).first()
                if user:
                    flash('Пользователь с такой почтой уже существует')
                    return redirect(url_for('registration'))
                else:
                    if request.form['password'] and request.form['repeat_password']:
                        if request.form['password'] != request.form['repeat_password']:
                            flash('Введённые пароли не совпадают')
                            return redirect(url_for('registration'))
                        else:
                            password = generate_password_hash(request.form['password'])
                            new_user = User(email=email, password=password)
                            db.session.add(new_user)
                            db.session.commit()
                            return redirect(url_for('start_page'))
                    else:
                        flash('Введите пароль')
                        return redirect(url_for('registration'))
            else:
                flash('Введите почту')
                return redirect(url_for('registration'))
        return render_template('registration_page.html')
    

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы разлогинились')
        return redirect(url_for('start_page'))
    
    
    return app
