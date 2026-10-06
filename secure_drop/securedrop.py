import cmd              #   For building shell
import readline         #   
import rlcompleter      #   rlcomplete for set_completer in readline module
import user             #   registration module for logging in/new users

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
        print("\"send\" -> Transfer fil to contact")
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

attempts = 0
#Registering
register = input('Do you want to register a user (y/n) ')
match register:
    # Registering case, when done will quit SecureDrop
    case 'y':
        user.register()
        exit(1)
    case 'n':
        print("Please login")
        for attempts in range(5):
            authenticated = False #signin(email, password)
            if attempts >= 4 :
                print("Too many attempts. Try again later.\n")
                exit(1)
            elif authenticated:
                if __name__ == '__main__':
                    SecureDrop().cmdloop()
    case _:
        print(f"Invalid input")
        exit(1)
