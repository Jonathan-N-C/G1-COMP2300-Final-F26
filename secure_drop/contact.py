import database
import getpass
import json

def addContact(contact_DB):
    database.ensure_DB(contact_DB)
    contactName = input('Enter Full Name: ')
    contactEmail = input('Enter Email Address: ').strip().lower() #normalize email: remove space, lowercase

    contactList = database.load_list(contact_DB)

    contactList.append({
            "fullName": contactName,
            "email": contactEmail,
            })
    with open(contact_DB,"w") as file:
        json.dump(contactList, file, indent=4)
    
    return