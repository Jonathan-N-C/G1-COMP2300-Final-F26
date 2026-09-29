import crypt
import json

attempts = 0

for  (int i = 0; i < 5; i++) {
    authenticated = signin(email, password)

    if (authenticated) {
        break;
    }
    failedauthetication(email, passwort)
}
print("Welcome to SecureDrop\n")
print("Type help for commands \n")

menu = input()
# switch (menu)
#     case add
#     case list
#     case send
#     case exit

