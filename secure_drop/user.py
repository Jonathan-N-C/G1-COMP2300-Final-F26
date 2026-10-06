import json
import crypt
import os

user_DB = "user.json"


def signin(email, password):
    with open("user_DB","r") as file:
        usersList = json.load(file)

    passwordHash = usersList[email]
    return

def register(email, password):
    if not os.path.exists(user_DB):
        return
    with open("user_DB", "w") as file:
        usersList = json.load(file)

    passwordHash = crypt.crypt(password)
    

    return