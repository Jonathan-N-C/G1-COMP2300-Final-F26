import os
import json

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