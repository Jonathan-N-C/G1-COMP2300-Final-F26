import os
import json
import base64
from Crypto.Cipher import AES

# Builds path from this file location, not current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_DB = os.path.join(BASE_DIR, "data", "user.json")
contact_DB = os.path.join(BASE_DIR, "data", "contact.json")

# check that a base exists, if not create a json file rready to receive a list
def ensure_db(dataFile):
    # creates the data directory and an empty user file if they are missing
    os.makedirs(os.path.dirname(dataFile), exist_ok=True)
    if not os.path.exists(dataFile):
        with open(dataFile, "w") as file:
            json.dump([], file)

# load users in the user dataFile
def load_list(dataFile):
    # returns a list of registered users, creates file first if needed
    ensure_db(dataFile)
    with open(dataFile, "r") as file:
        return json.load(file)

# check that dataFile has list
def has_list(dataFile):
    # return true if this client already has users registered
    return len(load_list(dataFile)) > 0

#load a list that is stored encrypted with AES-GCM, empty list if there is no file
def load_encrypted_list(dataFile, key):
    if not os.path.exists(dataFile):
        return[]
    with open(dataFile, "r") as file:
        stored = json.load(file)
    cipher = AES.new(key, AES.MODE_GCM, nonce=base64.b64decode(stored["nonce"]))
    # raises ValueError if the file was changed or the key is wrong
    plaintext = cipher.decrypt_and_verify(base64.b64decode(stored["ciphertext"]), base64.b64decode(stored["tag"]))
    return json.loads(plaintext)

#save a list encrypted with AES-GCM (confidentiality and integrity)
def save_encrypted_list(dataFile, key, data):
    os.makedirs(os.path.dirname(dataFile), exist_ok=True)
    cipher = AES.new(key, AES.MODE_GCM) # new random nonce every time
    ciphertext, tag = cipher.encrypt_and_digest(json.dumps(data).encode())
    stored = {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "tag": base64.b64encode(tag).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
    }
    with open(dataFile, "w") as file:
        json.dump(stored, file, indent=4)