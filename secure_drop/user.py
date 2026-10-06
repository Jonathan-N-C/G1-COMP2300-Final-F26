import crypt
import getpass
import json
import os

user_DB = "data/user.json"
class User:
    def __init__(self,  email, pwdHash):
        self.email = email
        self.pwdHash = pwdHash

def signin(email, password):
    with open("user_DB","r") as file:
        usersList = json.load(file)

    passwordHash = usersList[email]
    return

def register():
    # if not os.path.exists(user_DB):
        # return False
    with open(user_DB, "r") as file:
        usersList = json.load(file)

    regEmail = input('Enter email: ')
    regPwd = getpass.getpass('Enter password: ')
    if (regPwd == getpass.getpass('Re-enter password: ')):
        passwordHash = crypt.crypt(regPwd)
        newUser = User(regEmail, passwordHash)

        usersList.append(json.dumps(newUser.__dict__))
        with open(user_DB,"w") as file:
            json.dump(usersList, file, indent=4)
        
        print("Passwords Match.\nUser Registered.")
        return True

    print(f"Passwords didn't match. User not registered")
    return False