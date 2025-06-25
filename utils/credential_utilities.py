import os
import json

def get_user_file(username) :
    #uploading files to data path
    base_dir = os.path.join("data", username)
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "credentials.json")

def load_user_credentials(username) :
    # Get specified user file
    # Return an empty array if not found
    file = get_user_file(username)
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        return json.load(f)
    
def save_user_credentials(username, credential) :
    file = get_user_file(username)
    with open(file, 'w') as f:
        json.dump(credential, f)
