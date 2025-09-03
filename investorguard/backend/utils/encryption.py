# Encryption utils
from cryptography.fernet import Fernet
import base64

# Generate a key (in prod, store securely)
key = base64.urlsafe_b64encode(b'your_32_byte_key_here_1234567890')  # Change this
cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()