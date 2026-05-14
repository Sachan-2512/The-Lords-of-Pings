import socket
import threading
import json
from cryptography.fernet import Fernet

# Esta clave DEBE ser exactamente la misma que usa el cliente
CLAVE_COMPARTIDA = b'x_Yh5A9gO7tW_yRQ1P7w8Y6y2m_zS4w-1Sg1jA4U0o8='
cipher = Fernet(CLAVE_COMPARTIDA)

HOST = "127.0.0.1"  # Permite recibir conexiones desde cualquier IP en la red
PORT = 5050
BUFFER_SIZE = 1024


def handle_client(client_socket, client_address):
    ip_address = client_address[0]

    print(f"Hello {ip_address} welcome to the server!")

    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)

            if not data:
                break

            try:
                message = json.loads(data.decode("utf-8"))

                if (
                    isinstance(message, dict)
                    and "group" in message
                    and "payload" in message
                    and isinstance(message["group"], str)
                    and isinstance(message["payload"], str)
                ):
                    # Desencriptamos el payload que envió el cliente
                    try:
                        # Convertimos el string nuevamente a bytes, desencriptamos y luego lo pasamos a string
                        payload_encriptado = message["payload"].encode("utf-8")
                        payload_desencriptado = cipher.decrypt(payload_encriptado).decode("utf-8")
                        
                        print(f"{message['group']}: {payload_desencriptado}")
                    except Exception as e:
                        print(f"Error al desencriptar el mensaje de {ip_address}: {e}")
                else:
                    print(f"{ip_address} wants to send an ill formatted message.")

            except json.JSONDecodeError:
                print(f"{ip_address} wants to send an ill formatted message.")

    except ConnectionResetError:
        pass

    finally:
        print(f"Bye {ip_address}!")
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )

            client_thread.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
