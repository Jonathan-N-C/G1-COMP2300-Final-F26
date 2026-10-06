import crypt
import getpass
import json

user_DB = "data/user.json"
class User:
    def __init__(self,  email, pwdHash):
        self.email = email
        self.pwdHash = pwdHash

def signin():
    with open("user_DB","r") as file:
        usersList = json.load(file)
    inEmail = input('Enter email: ')
    if True:
        inPwdHash = getpass.getpass('Enter password: ')
        
    return False

def register():
    # if not os.path.exists(user_DB):
        # return False
    with open(user_DB, "r") as file:
        usersList = json.load(file)
    #  Get new user's email (ensure no existing user with same email)
    regEmail = input('Enter email: ')
    for user in usersList:
        if user["email"] == regEmail:
            print(f"Email is already registered!")
            return False
    # Set new user's password
    regPwd = getpass.getpass('Enter password: ')
    if (regPwd == getpass.getpass('Re-enter password: ')):
        passwordHash = crypt.crypt(regPwd)
        usersList.append({
            "email": regEmail,
            "pwdHash": passwordHash
        })
        with open(user_DB,"w") as file:
            json.dump(usersList, file, indent=4)
        print("Passwords Match.\nUser Registered.")
        return True

    print(f"Passwords didn't match. User not registered")
    return False