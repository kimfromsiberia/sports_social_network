from datetime import datetime
from flask import flash, Flask, redirect, request, url_for, render_template
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from sport_social_network.forms import SignInForm, SignUpForm, PersonSettingsForm, SportObjectSettingsForm
from sport_social_network.model import (
                                        db,
                                        User,
                                        Person,
                                        SportObject,
                                        friends,
                                        subscriptions,
                                        training_here,
                                        )
from sport_social_network.units import (get_guest_friends_list,
                                        get_current_user_friends_list,
                                        check_person_in_friends,
                                        add_user_in_friends,
                                        get_subscriptions_list,
                                        get_guest_subscriber_list,
                                        get_training_here_list,
                                        check_subscription,
                                        subscribe_to,
                                        get_training_places_list,
                                        get_persons_training_here_list,
                                        check_person_training_here,
                                        add_to_training_places,
                                        )


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
        if form.validate_on_submit():
            user = User.query.filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                if user.user_type == 'person':
                    if Person.query.filter(Person.id == user.id).first().name:
                        return redirect(url_for('user_page', user_id=user.id))
                    else:
                        flash('Заполните свои данные')
                        return redirect(url_for('user_settings', user_id=user.id))
                else:
                    if SportObject.query.filter(SportObject.id == user.id).first().name:
                        return redirect(url_for('user_page', user_id=user.id))
                    else:
                        flash('Заполните свои данные')
                        return redirect(url_for('user_settings', user_id=user.id))
            else:
                flash('Неправильная почта или пароль')
        return render_template('start_page.html', form=form)

    @app.route('/registration/', methods=['GET', 'POST'])
    def registration():
        form = SignUpForm()
        if form.validate_on_submit():
            email = form.email.data
            if email:
                person = User.query.filter(User.email == email).first()
                if person:
                    flash('Пользователь с такой почтой уже существует')
                    return redirect(url_for('registration'))
                else:
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
        return render_template('registration_page.html', form=form)

    @app.route('/so_registration/', methods=['GET', 'POST'])
    def so_registration():
        form = SignUpForm()
        if form.validate_on_submit():
            email = form.email.data
            if email:
                sport_object = User.query.filter(User.email == email).first()
                if sport_object:
                    flash('Пользователь с такой почтой уже существует')
                    return redirect(url_for('so_registration'))
                else:
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
        return render_template('so_registration_page.html', form=form)

    @app.route('/u_id<user_id>', methods=['GET', 'POST'])
    @login_required
    def user_page(user_id):
        try:
            if User.query.filter(User.id == user_id).first().user_type == 'person':
                user = Person.query.filter(Person.id == user_id).first()
                guest_friends_list = get_guest_friends_list(friends, user_id)
                current_user_friends_list = get_current_user_friends_list(friends, current_user)
                person_in_friends = check_person_in_friends(user_id, current_user_friends_list)
                current_user_subscriptions_list = get_subscriptions_list(subscriptions, current_user)
                current_user_training_places_list = get_training_places_list(training_here, current_user)
                if request.method == 'POST':
                    if request.form['add_friend_button']:
                        person_in_friends = True
                        flash(add_user_in_friends(user_id, current_user, current_user_friends_list))
                return render_template(
                    'user_page.html',
                    user=user,
                    friends_list=guest_friends_list,
                    user_id=user_id,
                    person_in_friends=person_in_friends,
                    current_user_subscriptions_list=current_user_subscriptions_list,
                    current_user_training_places_list=current_user_training_places_list,
                    )
            else:
                user = SportObject.query.filter(SportObject.id == user_id).first()
                guest_subscriber_list = get_guest_subscriber_list(subscriptions, user_id)
                current_user_subscriptions_list = get_subscriptions_list(subscriptions, current_user)
                training_here_list = get_training_here_list(training_here, user_id)
                subscription = check_subscription(user_id, current_user_subscriptions_list)
                current_user_training_places_list = get_training_places_list(training_here, current_user)
                persons_training_here_list = get_persons_training_here_list(training_here, user_id)
                person_training_here = check_person_training_here(user_id, current_user_training_places_list)
                if request.method == 'POST':
                    if request.form['submit'] == 'Подписаться':
                        subscription = True
                        flash(subscribe_to(user_id, current_user, current_user_subscriptions_list))
                    elif request.form['submit'] == 'Я тренируюсь здесь':
                        person_training_here = True
                        flash(add_to_training_places(user_id, current_user, current_user_training_places_list))
                    else:
                        None
                return render_template(
                    'so_user_page.html',
                    user=user,
                    user_id=int(user_id),
                    subscription=subscription,
                    current_user_subscriptions_list=current_user_subscriptions_list,
                    guest_subscriber_list=guest_subscriber_list,
                    training_here_list=training_here_list,
                    persons_training_here_list=persons_training_here_list,
                    person_training_here=person_training_here,
                    )
        except AttributeError:
            flash('Пользователя не существует')
            return redirect(url_for('start_page'))

    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    def user_settings():
        if User.query.filter(User.id == current_user.id).first().user_type == 'person':
            form = PersonSettingsForm()
            user = Person.query.filter(Person.id == current_user.id).first()
            if form.validate_on_submit():
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
            if form.validate_on_submit():
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

    @app.route('/u_id<user_id>/subscriptions/', methods=['GET', 'POST'])
    def person_subscriptions(user_id):
        subscriptions_list = get_subscriptions_list(subscriptions, current_user)
        sport_object_emails = []
        for sport_object_id in subscriptions_list:
            sport_object_emails.append(db.session.query(SportObject.email).filter(SportObject.id == sport_object_id).first()[0])
        return render_template('subscriptions.html', sport_object_emails=sport_object_emails, user_id=user_id)

    @app.route('/u_id<user_id>/training_here/', methods=['GET', 'POST'])
    def training(user_id):
        training_places_list = get_training_places_list(training_here, current_user)
        sport_object_emails = []
        for sport_object_id in training_places_list:
            sport_object_emails.append(db.session.query(SportObject.email).filter(SportObject.id == sport_object_id).first()[0])
        return render_template('training_here.html', sport_object_emails=sport_object_emails, user_id=user_id)

    @app.route('/u_id<user_id>/subscribers/', methods=['GET', 'POST'])
    def subscribers(user_id):
        subscribers_list = get_guest_subscriber_list(subscriptions, user_id)
        person_emails = []
        for person_id in subscribers_list:
            person_emails.append(db.session.query(Person.email).filter(Person.id == person_id).first()[0])
        return render_template('subscribers.html', person_emails=person_emails, user_id=user_id)

    @app.route('/u_id<user_id>/training_persons/', methods=['GET', 'POST'])
    def training_persons(user_id):
        training_here_list = get_training_here_list(training_here, user_id)
        person_emails = []
        for person_id in training_here_list:
            person_emails.append(db.session.query(Person.email).filter(Person.id == person_id).first()[0])
        return render_template('training_persons.html', person_emails=person_emails, user_id=user_id)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Вы разлогинились')
        return redirect(url_for('start_page'))

    return app
