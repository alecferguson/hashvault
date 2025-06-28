import os
import hashlib
import json
user_file = 'users.json'
current_user = None
user_data = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    global user_data
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            try:
                user_data = json.load(f)
            except json.JSONDecodeError:
                user_data = {}
    else: user_data = {}  

def save_users():
    with open(user_file, 'w') as f:
        json.dump(user_data,f,indent=4)

def users_exists(username):
    if not os.path.exists(user_file):
        return False
    with open(user_file,'r') as f:
        users = json.load(f)
    return username in users
   
    
def register(username, password):
    if users_exists(username):
        print("User already exisits")
        return 
    user_data[username] = {
            "password": hash_password(password),
            "services": {}}
    save_users()
    print("Registration Sucessful")

def login(username, password):
    global current_user
    load_users()

    hashed = hash_password(password)
    if username in user_data and user_data[username]["password"] == hashed:
        current_user = username
        print("Login successful")
    else: print("Login failed")

def addService(service, service_user, service_password):
    
    if not current_user:
        print("Please login in first")
        return
    hashed = hash_password(service_password)
    user_data[current_user]["services"][service] = {"username": service_user,
                                            "password": hashed}
    save_users()
    print(f"Service '{service}' added.")

def show_services():
    if not current_user:
        print("Please log in first.")
        return

    services = user_data[current_user].get("services", {})
    if not services:
        print("No services saved.")
    else:
        for name, creds in services.items():
            print(f"{name}: {creds['username']} / {creds['password']}")

