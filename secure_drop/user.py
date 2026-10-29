import crypt
import getpass
import json
import os
import re
from hmac import compare_digest as compare_hash
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

# Builds path from this file location, not current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_DB = os.path.join(BASE_DIR, "data", "user.json")

# check that a base exists, if not create a json file rready to receive a list
def ensure_db(database):
    # creates the data directory and an empty user file if they are missing
    os.makedirs(os.path.dirname(database), exist_ok=True)
    if not os.path.exists(database):
        with open(database, "w") as file:
            json.dump([], file)

# load users in the user database
def load_users():
    # returns a list of registered users, creates file first if needed
    ensure_db(user_DB)
    with open(user_DB, "r") as file:
        return json.load(file)

    # check that user database has users
def has_users():
    # return true if this client already has users registered
    return len(load_users()) > 0

#create rsa public and private keys
def create_key_pair():
     # key generation
    priv_key = RSA.generate(2048)
    pub_key = priv_key.public_key()

    # key stores
    priv_key_file = os.path.join(BASE_DIR, "data/keys", "id_rsa")
    with open(priv_key_file,"w") as file:
        file.write(priv_key.export_key().decode("utf-8"))

    pub_key_file = os.path.join(BASE_DIR, "data/keys", "id_rsa.pub")
    with open(pub_key_file,"w") as file:
        file.write(pub_key.export_key().decode("utf-8"))
    return

def signin():
    usersList = load_users()
    inEmail = input('Enter Email Address: ').strip().lower() #normalize email: remove space, lowercase
    for user in usersList:
        if user["email"] == inEmail:
            inPassword = getpass.getpass('Enter Password: ') 
            passwordCheck = compare_hash(crypt.crypt(inPassword, user["pwdHash"]), user["pwdHash"])  
            if passwordCheck:
                return True
            print(f"Incorrect Password")
    return False

def register():
    usersList = load_users()
    regName = input('Enter Full Name: ')

    #  Get new user's email (ensure no existing user with same email)
    # regex pattern matching the email input from the user
    emailPattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    while not re.match(emailPattern,
                       regEmail := input('Enter Email Address: ').strip().lower()
                       ): #spelling und lowercase
        print("Invalid Email, try again")
    for user in usersList:
        if user["email"] == regEmail:
            print(f"Email is already registered!")
            return False

    # Set new user's password
    regPwd = getpass.getpass('Enter Password: ')
    if not regPwd.strip(): #reject empty or whitespace-only passwords
        print('Empty password. User not registered')
        return False 
    if (regPwd == getpass.getpass('Re-enter Password: ')):
        #create passwordHash
        passwordHash = crypt.crypt(regPwd)

        create_key_pair()
        
        # Add user to user.json
        usersList.append({
            "fullName": regName,
            "email": regEmail,
            "pwdHash": passwordHash,
        })
        with open(user_DB,"w") as file:
            json.dump(usersList, file, indent=4)
        print("Passwords Match.\nUser Registered.")
        return True

    print(f"Passwords didn't match. User not registered")
    return False