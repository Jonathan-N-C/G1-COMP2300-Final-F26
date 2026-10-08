import cmd              #   For building shell
import readline         #   
import rlcompleter      #   rlcomplete for set_completer in readline module
import user             #   registration module for logging in/new users
import sys

# Shell for SecureDrop
# do_X methods are commands to be used
class SecureDrop(cmd.Cmd):
    # Shell displays secure_drop before input
    prompt = "secure_drop> "

    # Constructs a basic shell
    def __init__(self):
        super().__init__()
        readline.set_completer(rlcompleter.Completer(self.__dict__).complete)

    # Display all commands and descriptions
    def do_help(self, arg):
        """List all menu options"""
        print("\"add\" -> Add a new contact")
        print("\"list\" -> List all online contacts")
        print("\"send\" -> Transfer file to contact")
        print("\"exit\" -> Exit SecureDrop")

    # Adds a new contact
    def do_add(self, arg):
        """Add a new contact"""
        contactName = input('Enter Full Name: ')
        contactEmail = input('Enter email: ')
        print(f"Add")

    # Lists all online contacts
    def do_list(self, arg):
        """List all online contacts"""
        print(f"List")

    # Lists all online contacts
    def do_send(self, arg):
        """Send file to online contact"""
        print(f"Send")
    
    # Exits the shell
    def do_exit(self, arg):
        """Exit the shell"""
        print(f"Exiting...")
        return True

    # Catches all unknown inputs
    def default(self, arg):
        """Say invalid menu option to user"""
        print(f"Invalid Menu Option")

# registering
# Startup: registration on first run, login afterward
if not user.has_users():
    print("No users are registered with this client.")
    answer = input("Do you want to register a new user (y/n)? ").strip().lower()
    if answer == 'y':
        sys.exit(0 if user.register() else 1)
    sys.exit(1)

print("Please login")
for attempts in range(5):
    if attempts >= 4:
        print("Too many attempts. Try again later.\n")
        sys.exit(1)
    elif not user.signin():
        print("Failed sign in")
    else:
        if __name__ == '__main__':
            SecureDrop().cmdloop()
        sys.exit(0)

