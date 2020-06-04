import socket


def server_stop():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname + ".local")
    port = 10000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((host, port))
        c.sendall(b"bla")
