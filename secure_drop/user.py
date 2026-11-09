import crypt
import getpass
import json
import os
import re
import database
import base64
from hmac import compare_digest as compare_hash
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt


#create rsa public and private keys and save to data/keys in specified directory
def create_key_pair(directory, password):
     # key generation
    priv_key = RSA.generate(2048)
    pub_key = priv_key.public_key()

    # check if data exists
    keys_dir = os.path.join(directory, "data", "keys")
    os.makedirs(keys_dir, exist_ok=True)

    # store private key and encrypt with user's password
    with open(os.path.join(keys_dir, "id_rsa"), "w") as file:
        file.write(priv_key.export_key(passphrase=password, pkcs=8, protection="scryptAndAES128-CBC").decode("utf-8"))

    
    with open(os.path.join(keys_dir, "id_rsa.pub"),"w") as file:
        file.write(pub_key.export_key().decode("utf-8"))
    return

#unlock private key after successful login and derive the AES key
def load_session(user, password):
    # the private key is stored encrypted, the password unlocks it
    keys_dir = os.path.join(database.BASE_DIR, "data", "keys")
    with open(os.path.join(keys_dir, "id_rsa"), "r") as file:
        priv_key = RSA.import_key(file.read(), passphrase=password)

    # same password and same salt give the same AES key
    salt = base64.b64decode(user["kdfSalt"])
    aes_key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)

    return {"email": user["email"], "piv_key": priv_key, "aes_key": aes_key}

def signin(dataFile):
    usersList = database.load_list(dataFile)
    inEmail = input('Enter Email Address: ').strip().lower() #normalize email: remove space, lowercase
    inPassword = getpass.getpass('Enter Password: ') #always ask, so it doesn't reveal which emails exist
    for user in usersList:
        if user["email"] == inEmail:
            passwordCheck = compare_hash(crypt.crypt(inPassword, user["pwdHash"]), user["pwdHash"])  
            if passwordCheck:
                return load_session(user, inPassword)
    return None

def register(dataFile):
    usersList = database.load_list(dataFile)
    regName = input('Enter Full Name: ')

    # Get new user's email (ensure no existing user with same email)
    # regex pattern matching the email input from the user
    emailPattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    while not re.match(emailPattern,
                       regEmail := input('Enter Email Address: ').strip().lower()
                       ): #normalize email: remove space, lowercase
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
        #random salt which is used at login to derive the AES key from the password
        kdfSalt = get_random_bytes(16)

        create_key_pair(database.BASE_DIR, regPwd)
        
        # Add user to user.json
        usersList.append({
            "fullName": regName,
            "email": regEmail,
            "pwdHash": passwordHash,
            "kdfSalt": base64.b64encode(kdfSalt).decode(),
        })
        with open(dataFile,"w") as file:
            json.dump(usersList, file, indent=4)
        print("Passwords Match.\nUser Registered.")
        return True

    print(f"Passwords didn't match. User not registered")
    return False