import hashlib,json,rsa,base64,os
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet,MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def open_Key(name,password):
    key = b''
    with open(f"Keys/Remote_{name}.key",'rb') as f:
        key = f.read()
    keys = key.split(b'\n')
    keys[2] = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=keys[2],
        iterations=100000,
        backend=default_backend()
    )
    output = MultiFernet([
        Fernet(keys[0]),
        Fernet(keys[1]),
        Fernet(base64.urlsafe_b64encode(keys[2].derive(password)))
    ])
    return output

def hashString(text):
    result = hashlib.sha256(text.encode())
    return result.hexdigest()

def get_Config():
    output = {}
    with open("config.json",'r') as f:
        output = json.loads(f.read())
    return output

class Colors:
    GREEN = "\u001b[32m"
    RED = "\u001b[31m"
    BRED = "\u001b[31;1m"
    CYAN = "\u001b[36m"
    YELLOW = "\u001b[33m"
    BOLD = "\u001b[1m"
    BMAGENTA = "\u001b[35;1m"
    RESET = "\u001b[0m"