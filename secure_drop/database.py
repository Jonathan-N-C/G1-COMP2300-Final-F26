import os
import json

# check that a base exists, if not create a json file rready to receive a list
def ensure_db(database):
    # creates the data directory and an empty user file if they are missing
    os.makedirs(os.path.dirname(database), exist_ok=True)
    if not os.path.exists(database):
        with open(database, "w") as file:
            json.dump([], file)

# load users in the user database
def load_list(database):
    # returns a list of registered users, creates file first if needed
    ensure_db(database)
    with open(database, "r") as file:
        return json.load(file)

    # check that user database has users
def has_list(database):
    # return true if this client already has users registered
    return len(load_users(database)) > 0