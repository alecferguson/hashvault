# HashVault
HashVault is a simple and secure password manager built with Python and Tkinter.

## Features
GUI interface using TKinter.
Multi-User registration and login with hashed passwords using PBKDF2.
Local file-based storage using JSON.
Encryped service credentials using Fernet.

## Dependencies
python3 (windows)
Use exe on python website

python3 (linux)
sudo <package_manager> install python3
Note: some linux distributions do not install tkinter alongside so run,
sudo <package_manager> install python3-tk

Install cryptography (windows/linux)
pip install cryptography

## Installation 
git clone https://github.com/alecferguson/hashvault.git
cd hashvault
python app.py
