import hashlib,json,rsa,base64,os
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet,MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def GenKey(filename,size, name, password = b"Passw0rd"):
    remote = Fernet.generate_key()+b"\n"+Fernet.generate_key()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    with open(f"Data/Keys/{filename}.key",'wb') as f:
        f.write(remote+b'\n'+base64.urlsafe_b64encode(kdf.derive(password)))
    with open(f"Data/Keys/Remote_{name}.key",'wb') as f:
        f.write(remote+b'\n'+salt)

def open_Key(name):
    key = b''
    with open(f"Data/Keys/{name}.key",'rb') as f:
        key = f.read()
    keys = key.split(b'\n')
    output = MultiFernet([Fernet(keys[0]),Fernet(keys[1]),Fernet(keys[2])])
    return output

def hashString(text):
    result = hashlib.sha256(text.encode())
    return result.hexdigest()

def get_Config():
    output = {}
    with open("Data/config.json",'r') as f:
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