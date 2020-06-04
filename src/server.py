import socket


def server_start():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname + ".local")
    port = 10000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Created lobby on %s, port %s" % (host, port))
        print("Waiting for connection...")

        conn, addr = s.accept()
        print("Connected by ", addr)

        while True:
            data = conn.recv(1024)
            if not data and addr[0] == host:
                print("Requesting to stop server...")
                break
            elif data:
                print(data.decode())
    print("Lobby closed.")


def server_stop():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname + ".local")
    port = 10000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((host, port))
        c.sendall(b"")
