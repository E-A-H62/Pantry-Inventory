from project.models import fetch_user, add_user

def login(username, password):
    return fetch_user(username, password)

def sign_up(username, password, email):
    return add_user(username, password, email)




    