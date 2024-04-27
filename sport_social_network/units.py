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
        friend.followed.append(sender)
        db.session.commit()
        return 'Пользователь добавлен в друзья'
