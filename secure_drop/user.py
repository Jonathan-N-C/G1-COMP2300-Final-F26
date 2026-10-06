import crypt
import getpass
import json
from hmac import compare_digest as compare_hash
user_DB = "data/user.json"

def signin():
    with open(user_DB,"r") as file:
        usersList = json.load(file)
    inEmail = input('Enter email: ')
    for user in usersList:
        if user["email"] == inEmail:
            inPassword = getpass.getpass('Enter password: ')
            passwordCheck = compare_hash(crypt.crypt(inPassword, user["pwdHash"]), user["pwdHash"])  
            if passwordCheck:
                return True    
            print(f"Incorrect Password")
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