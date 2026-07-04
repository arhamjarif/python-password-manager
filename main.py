import os,base64,json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
def data_to_vault(vault:dict):
    with open('vault.json','wt') as file:
        json.dump(vault,file)

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
