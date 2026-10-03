# import crypt
import cmd              #   For building shell
import readline         #   
import rlcompleter      #   rlcomplete for set_completer in readline module

attempts = 0
#Registering
print("Do you want to register a user (y/n)")
register = input()
match register:
    # Registering case, when done will quit SecureDrop
    case 'y':
        print("Enter Full Name: ")
        print("Enter Email Address: ")
        print("Enter Password: ")
        print("Re-enter Password: ")
        exit(1)
    #
    case 'n':
        print("Please login")
        for attempts in range(5):
            authenticated = False #signin(email, password)
            if attempts >= 4 :
                print("Too many attempts. Try again later.\n")
                exit(1)
        # failedAuthetication(email, password)


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
        print(f"Add")

    # Lists all online contacts
    def do_list(self, arg):
        """List all online contacts"""
        print(f"List")

    # Exits the shell
    def do_exit(self, arg):
        """Exit the shell"""
        print(f"Exiting...")
        return True

    # Catches all unknown inputs
    def default(self, arg):
        """Say invalid menu option to user"""
        print(f"Invalid Menu Option")

if __name__ == '__main__':
    SecureDrop().cmdloop()