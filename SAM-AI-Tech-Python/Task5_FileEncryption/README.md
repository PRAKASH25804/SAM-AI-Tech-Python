# Task 5 — Python File Encryption / Decryption

A secure utility for encrypting and decrypting text files with password protection.

## Features

- Encrypt `.txt` files
- Decrypt encrypted files
- Password protection
- Save encrypted output
- Error handling for missing files and invalid passwords

## Requirements

- Python 3.8+
- `cryptography`

## Install

```bash
python -m pip install --upgrade pip
python -m pip install cryptography
```

## Run

Encrypt a file:

```bash
python main.py encrypt sample.txt MySecurePassword
```

Decrypt a file:

```bash
python main.py decrypt sample.txt.enc MySecurePassword
```

Optional output path:

```bash
python main.py encrypt sample.txt MySecurePassword --output encrypted_file.enc
```

## Notes

The encrypted file format stores a randomly generated salt and a secure Fernet token. The password is derived using PBKDF2.
