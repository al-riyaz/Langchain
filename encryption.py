from cryptography.fernet import Fernet; 
print(Fernet.generate_key().decode())

'''import os
from cryptography.fernet import Fernet

decryption_key = os.environ["OPENAPI_DECRYPTION_KEY"]  # must exist in OS env
cipher = Fernet(decryption_key.encode())

secret = input("Enter secret to encrypt: ").encode()
encrypted = cipher.encrypt(secret).decode()

print("\nEncrypted value (store this in .env):")
print(encrypted)'''

import certifi
print(certifi.where())
