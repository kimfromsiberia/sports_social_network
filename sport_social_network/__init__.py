from datetime import datetime
from flask import flash, Flask, redirect, request, url_for, render_template
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from sport_social_network.forms import SignInForm, SignUpForm, PersonSettingsForm, SportObjectSettingsForm
from sport_social_network.model import db, User, Person, SportObject, friends


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
            return redirect((url_for('user_page', user_id=current_user.id)))
        form = SignInForm()
        if form.validate_on_submit:
            user = User.query.filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('user_page', user_id=user.id))
        return render_template('start_page.html', form=form)

    @app.route('/registration/', methods=['GET', 'POST'])
    def registration():
        form = SignUpForm()
        if form.validate_on_submit:
            email = form.email.data
            if email:
                person = User.query.filter(User.email == email).first()
                if person:
                    flash('Пользователь с такой почтой уже существует')
                    return redirect(url_for('registration'))
                else:
                    if form.password.data and form.confirm_password.data:
                        if form.password.data != form.confirm_password.data:
                            flash('Введённые пароли не совпадают')
                            return redirect(url_for('registration'))
                        else:
                            password = generate_password_hash(form.password.data)
                            new_person = Person(email=email, password=password, user_type='person')
                            db.session.add(new_person)
                            db.session.commit()
                            flash('Вы успешно зарегистрировались.')
                            return redirect(url_for('start_page'))
                    else:
                        flash('Введите пароль')
                        return redirect(url_for('registration'))
        return render_template('registration_page.html', form=form)

    @app.route('/so_registration/', methods=['GET', 'POST'])
    def so_registration():
        form = SignUpForm()
        if form.validate_on_submit:
            email = form.email.data
            if email:
                sport_object = User.query.filter(User.email == email).first()
                if sport_object:
                    flash('Пользователь с такой почтой уже существует')
                    return redirect(url_for('so_registration'))
                else:
                    if form.password.data and form.confirm_password.data:
                        if form.password.data != form.confirm_password.data:
                            flash('Введённые пароли не совпадают')
                            return redirect(url_for('so_registration'))
                        else:
                            password = generate_password_hash(form.password.data)
                            new_sport_object = SportObject(email=email, password=password, user_type='sport_object')
                            db.session.add(new_sport_object)
                            db.session.commit()
                            flash('Вы успешно зарегистрировались.')
                            return redirect(url_for('start_page'))
                    else:
                        flash('Введите пароль')
                        return redirect(url_for('so_registration'))
        return render_template('so_registration_page.html', form=form)

    @app.route('/u_id<user_id>', methods=['GET', 'POST'])
    @login_required
    def user_page(user_id):
        try:
            if User.query.filter(User.id == user_id).first().user_type == 'person':
                guest_friends_list = [friend[1] for friend in db.session.query(friends).filter(friends.c.sender_id == user_id)]
                current_user_friends_list = [friend[1] for friend in db.session.query(friends).filter(friends.c.sender_id == current_user.id)]
                if int(user_id) in current_user_friends_list:
                    person_in_friends = True
                else:
                    person_in_friends = False
                print(person_in_friends)
                user = Person.query.filter(Person.id == user_id).first_or_404()
                if request.method == 'POST':
                    if request.form['add_friend_button']:
                        if int(user_id) not in current_user_friends_list:
                            flash('Пользователь добавлен в друзья')
                            friend = Person.query.filter(Person.id == current_user.id).first()
                            sender = Person.query.filter(Person.id == user_id).first()
                            friend.followed.append(sender)
                            db.session.commit()
                return render_template(
                    'user_page.html',
                    user=user,
                    friends_list=guest_friends_list,
                    user_id=user_id,
                    person_in_friends=person_in_friends
                    )
            else:
                user = SportObject.query.filter(SportObject.id == user_id).first_or_404()
                return render_template(
                    'so_user_page.html',
                    user=user
                    )
        except:
            flash('Пользователя не существует')
            return redirect(url_for('start_page'))

    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    def user_settings():
        if User.query.filter(User.id == current_user.id).first().user_type == 'person':
            form = PersonSettingsForm()
            user = Person.query.filter(Person.id == current_user.id).first()
            if form.is_submitted():
                user.name = form.name.data
                user.last_name = form.last_name.data
                if form.date_of_birth.data:
                    try:
                        date = datetime.strptime(form.date_of_birth.data, '%d.%m.%Y')
                        user.date_of_birth = date
                    except ValueError:
                        flash('Неверный формат даты')
                user.country = form.country.data
                user.city = form.city.data
                db.session.commit()
                flash('Изменения сохранены')
            return render_template('user_settings.html', user=user, form=form)
        else:
            form = SportObjectSettingsForm()
            user = SportObject.query.filter(SportObject.id == current_user.id).first()
            if form.is_submitted():
                user.name = form.name.data
                user.country = form.country.data
                user.city = form.city.data
                user.address = form.address.data
                user.phone = form.phone.data
                db.session.commit()
                flash('Изменения сохранены')
            return render_template('so_user_settings.html', user=user, form=form)

    @app.route('/u_id<user_id>/friends/', methods=['GET', 'POST'])
    def person_friends(user_id):
        friends_list = [user[1] for user in db.session.query(friends).filter(friends.c.sender_id == current_user.id)]
        friends_email = []
        for friend_id in friends_list:
            friends_email.append(db.session.query(Person.email).filter(Person.id == friend_id).first()[0])
        return render_template('friends.html', friends_email=friends_email, user_id=user_id)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Вы разлогинились')
        return redirect(url_for('start_page'))

    return app
