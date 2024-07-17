from project.models import fetch_user_id, add_user


def sign_in(username, password):
    return fetch_user_id(username, password)


def sign_up(username, password, email):
    return add_user(username, password, email)
