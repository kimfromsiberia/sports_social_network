from datetime import datetime
from flask import flash, Flask, redirect, request, url_for, render_template
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from sport_social_network.model import db, User, Person, SportObject


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
        if request.method == 'POST':
            email = request.form['email']
            if email:
                user = User.query.filter(User.email == email).first()
                if user:
                    if user.check_password(request.form['password']):
                        login_user(user)
                        return redirect(url_for('user_page', user_id=user.id))
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
                user = Person.query.filter(Person.email == email).first()
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
                            new_user = Person(email=email, password=password, user_type='person')
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

    @app.route('/so_registration/', methods=['GET', 'POST'])
    def so_registration():
        if request.method == 'POST':
            email = request.form['email']
            if email:
                user = SportObject.query.filter(SportObject.email == email).first()
                if user:
                    flash('Пользователь с такой почтой уже существует')
                    return redirect(url_for('so_registration'))
                else:
                    if request.form['password'] and request.form['repeat_password']:
                        if request.form['password'] != request.form['repeat_password']:
                            flash('Введённые пароли не совпадают')
                            return redirect(url_for('so_registration'))
                        else:
                            password = generate_password_hash(request.form['password'])
                            new_user = SportObject(email=email, password=password, user_type='sport_object')
                            db.session.add(new_user)
                            db.session.commit()
                            return redirect(url_for('start_page'))
                    else:
                        flash('Введите пароль')
                        return redirect(url_for('so_registration'))
            else:
                flash('Введите почту')
                return redirect(url_for('so_registration'))
        return render_template('so_registration_page.html')

    @app.route('/u_id<user_id>')
    @login_required
    def user_page(user_id):
        if User.query.filter(User.id == user_id).first().user_type == 'person':
            user = Person.query.filter(Person.id == user_id).first_or_404()
            return render_template(
                'user_page.html',
                user=user
                )
        else:
            user = SportObject.query.filter(SportObject.id == user_id).first_or_404()
            return render_template(
                'so_user_page.html',
                user=user
                )

    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    def user_settings():
        if User.query.filter(User.id == current_user.id).first().user_type == 'person':
            user = Person.query.filter(Person.id == current_user.id).first()
            if request.method == 'POST':
                user.name = request.form['name']
                user.last_name = request.form['last_name']
                if request.form['date_of_birth']:
                    try:
                        date = datetime.strptime(request.form['date_of_birth'], '%d.%m.%Y')
                        user.date_of_birth = date
                    except ValueError:
                        flash('Неверный формат даты')
                user.country = request.form['country']
                user.city = request.form['city']
                db.session.commit()
                flash('Изменения сохранены')
            return render_template('user_settings.html', user=user)
        else:
            user = SportObject.query.filter(SportObject.id == current_user.id).first()
            if request.method == 'POST':
                user.name = request.form['name']
                user.country = request.form['country']
                user.city = request.form['city']
                user.address = request.form['address']
                db.session.commit()
                flash('Изменения сохранены')
            return render_template('so_user_settings.html', user=user)

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы разлогинились')
        return redirect(url_for('start_page'))

    return app
