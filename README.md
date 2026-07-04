# Password Manager

A terminal-based password manager built in Python that securely stores credentials using modern cryptographic techniques.

The application encrypts all stored credentials using **Fernet symmetric encryption**, while the encryption key is derived from the user's master password using **PBKDF2-HMAC-SHA256** with a randomly generated salt. The vault remains encrypted on disk at all times and is only decrypted in memory after successful authentication.

---

## Features

- Create a password vault protected by a master password
- Authenticate users before granting access to stored credentials
- Add new password entries
- View stored passwords
- Delete existing password entries
- Automatically encrypt and save the vault after every modification
- Generate a unique random salt for every vault
- Store all data in an encrypted JSON file

---

## Technologies Used

- Python 3
- cryptography
- PBKDF2-HMAC-SHA256
- Fernet
- JSON
- Base64 Encoding

---
## Requirements

- Python 3.12 or newer
- cryptography

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## How It Works

### Vault Creation

1. The user chooses a master password.
2. A random 16-byte salt is generated.
3. PBKDF2 derives a 256-bit encryption key from the master password and salt.
4. An empty password vault is encrypted using Fernet.
5. The encrypted vault and encoded salt are stored in `vault.json`.

### Authentication

1. The stored salt is loaded from the vault.
2. The user enters the master password.
3. PBKDF2 derives the encryption key using the entered password and stored salt.
4. Fernet attempts to decrypt the vault.
5. If decryption succeeds, the user is authenticated.
6. If decryption fails, access is denied.

### Managing Passwords

After successful authentication, the vault is decrypted into memory where the user may:

- Add new credentials
- View saved credentials
- Delete existing credentials

Every modification is immediately encrypted and written back to the vault to prevent data loss.

---

## Project Structure

```
password-manager/
│
├── password_manager.py
├── vault.json
├── README.md
├── .gitignore
└── .venv/          (local virtual environment, not committed)
```

---

## Security Notes

- Passwords are never stored in plaintext on disk.
- Encryption keys are never stored.
- The encryption key is derived each time the user authenticates.
- Every vault uses a unique randomly generated salt.
- Vault contents are encrypted using authenticated symmetric encryption (Fernet).
- The vault is automatically re-encrypted after every modification.

---

## Concepts Demonstrated

- Symmetric encryption
- Password-based key derivation
- Secure credential storage
- JSON serialization
- Base64 encoding and decoding
- File handling
- Exception handling
- Dictionary-based data structures
- Modular program design

---

## What I Learned

Building this project helped me gain practical experience with:

- The difference between **hashing** and **encryption**, and when each should be used.
- Deriving cryptographic keys securely using **PBKDF2** instead of creating keys manually.
- Using **Fernet** to perform authenticated symmetric encryption and decryption.
- Handling binary data by encoding and decoding it with Base64 for JSON storage.
- Designing an application that keeps sensitive data encrypted on disk while only decrypting it temporarily in memory.
- Organizing a larger Python project into modular functions with clear responsibilities.
- Working with third-party Python libraries inside a virtual environment.

---

## Future Improvements

- Edit existing password entries
- Password generator
- Hidden password input (`getpass`)
- Search functionality
- Duplicate entry overwrite confirmation
- Improved terminal interface

---

## Disclaimer

This project was built for educational purposes to explore cryptography, secure credential storage, and Python application design. It is not intended to replace production-ready password management software.
