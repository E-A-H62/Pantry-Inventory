from project import db
from project.models import fetch_user, fetch_user_id, add_user


def sign_in(username, password):
    return fetch_user_id(username, password)


def sign_up(username, password, email):
    return add_user(username, password, email)


def change_username(user_id, username):
    user = fetch_user(user_id)

    user.username = username

    db.session.commit()


def change_email(user_id, email):
    user = fetch_user(user_id)

    user.email = email

    db.session.commit()


def change_password(user_id, password):
    user = fetch_user(user_id)

    user.password = password

    db.session.commit()
