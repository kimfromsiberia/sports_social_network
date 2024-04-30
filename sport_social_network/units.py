from sport_social_network.model import db, Person, SportObject, User


def get_guest_friends_list(friends, user_id):
    return [friend[1] for friend in db.session.query(friends).filter(friends.c.sender_id == user_id)]


def get_current_user_friends_list(friends, current_user):
    return [friend[1] for friend in db.session.query(friends).filter(friends.c.sender_id == current_user.id)]


def check_person_in_friends(user_id, current_user_friends_list):
    return True if int(user_id) in current_user_friends_list else False


def add_user_in_friends(user_id, current_user, current_user_friends_list):
    if int(user_id) not in current_user_friends_list:
        friend = Person.query.filter(Person.id == current_user.id).first()
        sender = Person.query.filter(Person.id == user_id).first()
        friend.friendship.append(sender)
        db.session.commit()
        return 'Пользователь добавлен в друзья'


def get_subscriptions_list(subscriptions, current_user):
    return [follower[1] for follower in db.session.query(subscriptions).filter(subscriptions.c.person_id == current_user.id)]


def get_guest_subscriber_list(followers, user_id):
    return [follower[0] for follower in db.session.query(followers).filter(followers.c.sport_object_id == user_id)]


def get_training_here_list(training_here, user_id):
    return [person[0] for person in db.session.query(training_here).filter(training_here.c.sport_object_id == user_id)]


def check_subscription(user_id, current_user_subscriptions_list):
    return True if int(user_id) in current_user_subscriptions_list else False


def subscribe_to(user_id, current_user, current_user_subscriptions_list):
    if int(user_id) not in current_user_subscriptions_list:
        sender = Person.query.filter(Person.id == current_user.id).first()
        recipient = SportObject.query.filter(SportObject.id == user_id).first()
        sender.subscribe.append(recipient)
        db.session.commit()
        return 'Вы подписались'


def get_training_places_list(training_here, current_user):
    return [sport_object[1] for sport_object in db.session.query(training_here).filter(training_here.c.person_id == current_user.id)]


def get_persons_training_here_list(training_here, user_id):
    return [sport_object[0] for sport_object in db.session.query(training_here).filter(training_here.c.sport_object_id == user_id)]


def check_person_training_here(user_id, current_user_training_places_list):
    return True if int(user_id) in current_user_training_places_list else False


def add_to_training_places(user_id, current_user, current_user_training_places_list):
    if int(user_id) not in current_user_training_places_list:
        sender = Person.query.filter(Person.id == current_user.id).first()
        recipient = SportObject.query.filter(SportObject.id == user_id).first()
        sender.training.append(recipient)
        db.session.commit()
        return f'Теперь вы тренируетесь в {recipient.name}'
