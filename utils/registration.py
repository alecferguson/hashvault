import os
import hashlib
user_file = 'users.json'


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def users_exists(username):
    if not os.path.exists(user_file):
        return False
    with open(user_file,'r') as f:
        return any(line.startswith()(f"{username}:") for line in f)
    
def register():
    username = input("Enter username: ")
    if users_exists(username):
        print("User already exisits")
        return 
    password = input("Enter a new password: ")
    with open(user_file, 'a') as f:
        f.write(f"{username}:{hash_password(password)}\n")
    print("Registration Sucessful")

def login():
    if not os.path.exists(user_file):
        print("No users registered")

    username = input("Enter username")
    password = input("Enter the password: ")
    hashed = hash_password(password)
    with open(user_file, 'r') as f:
        for line in f:
            if line.strip() == f"{username}:{hash_password}":
                print("login successful")
    print("login failed")

def main():
    options = {'1': register, '2': login, '3': exit}
    while True:
        print("\n 1.Resgier\n 2.Login\n 3.exit")
        choice = input("choose an option: ")
        action = options.get(choice)
        if action:  
            action()
        else:
            print("invalid option")

if __name__ == "__main__":
    main()