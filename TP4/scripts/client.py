import socket
import json
from cryptography.fernet import Fernet


CLAVE_COMPARTIDA = b'x_Yh5A9gO7tW_yRQ1P7w8Y6y2m_zS4w-1Sg1jA4U0o8='
cipher = Fernet(CLAVE_COMPARTIDA)

HOST = "127.1.1.1"  
PORT = 5050         

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    user_input = input("Ingresa tu mensaje (o escribe 'adios' para salir): ")
    user_input_encrypted = cipher.encrypt(user_input.encode("utf-8"))

    if user_input.strip().lower() == 'adios':
        print("Cerrando conexión...")
        client.close()
        break

    message = {
        "group": "The Lords of Pings",
        "payload": user_input_encrypted.decode("utf-8")
    }

    client.sendall(json.dumps(message).encode("utf-8"))


 
