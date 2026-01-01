import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet
SERVER_IP = "127.0.0.1"   
PORT = 5000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
public_key_bytes = client.recv(2048)
public_key = serialization.load_pem_public_key(public_key_bytes)
aes_key = Fernet.generate_key()
fernet = Fernet(aes_key)
encrypted_aes_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
client.send(encrypted_aes_key)
message = input("Enter message: ")
encrypted_msg = fernet.encrypt(message.encode())
client.send(encrypted_msg)
print("Message sent securely")
client.close()