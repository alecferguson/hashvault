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
    load_users()
    if users_exists(username):
        return False, "User already exists"
    user_data[username] = {
            "password": hash_password(password),
            "services": {}}
    save_users()
    return True, "User registered successfully"

def authenticate(username, password):
    load_users()
    hashed = hash_password(password)
    if username in user_data and user_data[username]["password"] == hashed:
        return True
    return False