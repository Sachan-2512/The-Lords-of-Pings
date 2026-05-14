import socket
import json


HOST = "34.68.162.122"
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


while True:
    user_input = input("Ingresa tu mensaje (o escribe 'adios' para salir): ")
    
    if user_input.strip().lower() == 'adios':
        print("Cerrando conexión...")
        client.close()
        break

    message = {
        "group": "The Lords of Pings",
        "payload": user_input
    }

    client.sendall(json.dumps(message).encode("utf-8"))


 
