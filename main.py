import os,base64,json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken

def vault_data_to_vault(vault:dict):
    with open('vault.json','wt') as file:
        json.dump(vault,file)

def save_to_vault(master_password:str,salt:bytes,vault_data:dict):
    kdf = PBKDF2HMAC(algorithm= hashes.SHA256(), length=32,salt=salt,iterations=1200000)
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    encryptor = Fernet(key)
    encrypted_vault_data = encryptor.encrypt(json.dumps(vault_data).encode())
    vault = {
        'salt' : base64.urlsafe_b64encode(salt).decode(),
        'vault_data' : base64.urlsafe_b64encode(encrypted_vault_data).decode()
    }
    vault_data_to_vault(vault)

def add(vault_data:dict,master_password:str,salt:bytes):
    print('\n\n========== ADD PASSWORD ==========\n\n')
    service = input('Service of this new entry: ')
    username = input('Enter username: ')
    password = input('Enter password: ')
    if service in vault_data:
        print('Service already exists')
    else:
        vault_data[service] = (username,password)
        save_to_vault(master_password,salt,vault_data)
        print('\n\nEntry added to vault\n')

def view(vault_data:dict):
    print('\n\n========== VIEW PASSWORDS ==========\n\n')
    if vault_data:
        i = 0
        print()
        for key,value in vault_data.items():
            i += 1
            print('----------------------------------')
            print(f'Entry {i}:\n\n    Service: {key}\n    Username: {value[0]}\n    Password: {value[1]}\n')
            print('----------------------------------')
    else:
        print('No passwords stored')

def delete(vault_data:dict,master_password:str,salt:bytes):
    print('\n\n========== DELETE PASSWORD ==========\n\n')
    if vault_data:
        print('Saved services:\n')
        for service in vault_data.keys():
            print(service)
        del_choice = input('\nEnter service to delete: ')
        if del_choice in vault_data:
            del vault_data[del_choice]
            save_to_vault(master_password,salt,vault_data)
            print(f'\n{del_choice} successfully deleted')
        else:
            print('\nService not found')
    else:
        print('No passwords stored to delete')




print('========== PASSWORD MANAGER ==========\n\n')

if not os.path.exists('vault.json'): #no vault = vault creation
    print('No vault found. Would you like to create a vault?\n1.Yes\n2.No')
    if '1' == input('Enter your choice[1,2]: '):
        #vault creation
        while True:
            print('\n\n========== VAULT CREATION ==========\n\n')
            master_password = input('Enter master password: ')
            if master_password == input('Enter master password again: '):
                salt = os.urandom(16)
                vault_data = json.dumps({}).encode()
                kdf = PBKDF2HMAC(algorithm= hashes.SHA256(), length=32,salt=salt,iterations=1200000)
                key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
                encryptor = Fernet(key)
                encrypted_vault_data = encryptor.encrypt(vault_data)
                vault = {
                    'salt' : base64.urlsafe_b64encode(salt).decode(),
                    'vault_data' : base64.urlsafe_b64encode(encrypted_vault_data).decode()
                }
                vault_data_to_vault(vault)
                break
            else:
                print('Entered password did not match. Please try again')
else:
    print('\n\n========== AUTHENTICATION ==========\n\n')
    master_password = input('Enter password: ')
    vault = None
    with open('vault.json') as file:
        vault = json.load(file)
    salt = base64.urlsafe_b64decode(vault['salt'].encode())
    encrypted_vault_data = base64.urlsafe_b64decode(vault['vault_data'].encode())
    kdf = PBKDF2HMAC(algorithm= hashes.SHA256(), length=32,salt=salt,iterations=1200000)
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    decryptor = Fernet(key)
    try:
        vault_data_in_bytes = decryptor.decrypt(encrypted_vault_data)
        print('\nAuthentication successful')
        vault_data = json.loads(vault_data_in_bytes.decode())
        while True:
            print('\n\n========== MENU ==========\n\n')
            print('1. Add password\n2. View saved passwords\n3. Delete a saved password\n4. Exit')
            match input('Enter your choice: '):
                case '1':
                    add(vault_data,master_password,salt)
                case '2':
                    view(vault_data)
                case '3':
                    delete(vault_data,master_password,salt)
                case '4':
                    break
                case _:
                    print('Invalid choice. Try again.')

    except InvalidToken:
        print('Wrong password')