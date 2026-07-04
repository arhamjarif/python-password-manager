import os,base64,json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken

def data_to_vault(vault:dict):
    with open('vault.json','wt') as file:
        json.dump(vault,file)

def save_to_vault(master_password:str,salt:bytes,data:dict):
    kdf = PBKDF2HMAC(algorithm= hashes.SHA256(), length=32,salt=salt,iterations=50000)
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    encryptor = Fernet(key)
    encrypted_data = encryptor.encrypt(json.dumps(data).encode())
    vault = {
        'salt' : base64.urlsafe_b64encode(salt).decode(),
        'data' : base64.urlsafe_b64encode(encrypted_data).decode()
    }
    data_to_vault(vault)

def add(data:dict,master_password:str,salt:bytes):
    service = input('Service of this new entry: ')
    username = input('Enter username: ')
    password = input('Enter password: ')
    data[service] = (username,password)
    save_to_vault(master_password,salt,data)
    print('\n\nEntry added to vault\n')

def view(data:dict):
    i = 0
    for key,value in data.items():
        i += 1
        print(f'Entry {i}:\n\n    Service: {key}\n    Username: {value[0]}\n    Password: {value[1]}\n')

if not os.path.exists('vault.json'): #no vault = vault creation
    print('No vault found. Would you like to create a vault?\n1.Yes\n2.No')
    if '1' == input('Enter your choice[1,2]: '):
        #vault creation
        while True:
            master_password = input('Enter master password: ')
            if master_password == input('Enter master password again: '):
                salt = os.urandom(16)
                data = json.dumps({}).encode()
                kdf = PBKDF2HMAC(algorithm= hashes.SHA256(), length=32,salt=salt,iterations=50000)
                key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
                encryptor = Fernet(key)
                encrypted_data = encryptor.encrypt(data)
                vault = {
                    'salt' : base64.urlsafe_b64encode(salt).decode(),
                    'data' : base64.urlsafe_b64encode(encrypted_data).decode()
                }
                data_to_vault(vault)
                break
            else:
                print('Entered password did not match. Please try again')
else:
    master_password = input('Enter password: ')
    vault = None
    with open('vault.json') as file:
        vault = json.load(file)
    salt = base64.urlsafe_b64decode(vault['salt'].encode())
    encrypted_data = base64.urlsafe_b64decode(vault['data'].encode())
    kdf = PBKDF2HMAC(algorithm= hashes.SHA256(), length=32,salt=salt,iterations=50000)
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    decryptor = Fernet(key)
    try:
        data_in_bytes = decryptor.decrypt(encrypted_data)
        data = json.loads(data_in_bytes.decode())
        while True:
            print('1. Add password\n2. View saved passwords\n3. Delete a saved password\n4. Exit')
            match input('Enter your choice: '):
                case '1':
                    add(data,master_password,salt)
                case '2':
                    view(data)
                case '3':
                    delete()
                case '4':
                    break
                case _:
                    print('Invalid choice. Try again.')

    except InvalidToken:
        print('Wrong password')