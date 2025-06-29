# HashVault

HashVault is a simple and secure password manager built with Python and Tkinter.

## Features

- Graphical User Interface (GUI) using Tkinter  
- Multi-user registration and login with password hashing (hashlib)  
- Local file-based storage using JSON  
- Encrypted service credentials using Fernet (from the cryptography package)  

## Dependencies

### Python 3

Windows:  
Download and install Python 3 from the official website:  
https://www.python.org/downloads/windows/

Linux:  
Use your distribution's package manager to install Python 3:  
sudo <package_manager> install python3

Note: Some Linux distributions do not include Tkinter by default. If it's missing, install it using:  
sudo <package_manager> install python3-tk

### Cryptography Package

Install the cryptography package on both Windows and Linux:  
pip install cryptography

## Installation

1. Clone the repository:  
git clone https://github.com/alecferguson/hashvault.git

2. Navigate to the project directory:  
cd hashvault

3. Run the application:  
python app.py
