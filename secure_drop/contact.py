import database

def addContact(contact_DB, key):

    contactName = input('Enter Full Name: ')
    contactEmail = input('Enter Email Address: ').strip().lower() #normalize email: remove space, lowercase

    try:
        contactList = database.load_encrypted_list(contact_DB, key)
    except (ValueError, KeyError, TypeError):
        print("Contact list could not be verified, it may have been tampered with.")
        return False

    #drop any existing contact with this email, so the new details replace it
    contactList = [c for c in contactList if c["email"] != contactEmail]

    contactList.append({
            "fullName": contactName,
            "email": contactEmail,
            })
    database.save_encrypted_list(contact_DB, key, contactList)
    return True

# check the (encrypted) contact list for an email
# used when another client asks "have you added me?"
def isContact(contact_DB, key, email):
    try:
        contactList = database.load_encrypted_list(contact_DB, key)
    except (ValueError, KeyError, TypeError):
        return False
    email = email.strip().lower()
    return any(c["email"] == email for c in contactList)