import socket
import threading

def cli():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.2.13", 5555))
    print("Connected")

    msg = client_socket.recv(1024)
    print(msg)
    
def t():
    client = threading.Thread(target=cli, args=[])
    client.start()