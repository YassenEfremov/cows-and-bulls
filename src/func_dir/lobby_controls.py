import socket
import random
import threading

from func_dir.get_lan_ips import *
from func_dir.start_game import *


"""
+-------------------------------+
|      IMPORTANT KEYWORDS       |
|                               |
| SO - socket object            |
+-------------------------------+
"""

# Game parameters

PLAYER_NAME = "Player" + str(random.randint(1, 100))
'''
# Check parameters

try:
    opts, args = getopt.getopt(sys.argv[1:], "s", ["host=", "port=", "name="])

except getopt.GetoptError:
    print(__file__ + " [-s] [--host HOST_NAME] [--port PORT_NUMBER] [--name PLAYER_NAME]")
    sys.exit(2)
    
for opt, arg in opts:
    if opt == "-s":
        IS_SERVER = True

    if opt == "--host":
        host = arg

    if opt == "--port":
        port = int(arg)

    if opt == "--name":
        PLAYER_NAME = arg
'''
#   Get host info and LAN IPs   #

host_name = socket.gethostname()  # Alone seen as localhost
host = socket.gethostbyname(host_name + ".local")
port = 5555

devices = get_lan_ips()
print("LAN devices: ", devices)


#   Main lobby functions   #

def create_lobby_thread():
    """
    Creates a server SO which is bound to the host's IP address (+ a custom port) and awaits connections.
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Waiting for opponent to join...")

    conn_socket, addr = server_socket.accept()

    if addr[0] == host:
        print("Server closed")
        server_socket.close()

    else:
        # conn_socket.sendall(b"response")
        print("Opponent connected from ", addr)
        start_game(PLAYER_NAME, conn_socket)


def create_lobby():
    """
    Calls the above function in a separate thread to avoid halt.
    """

    lobby = threading.Thread(target=create_lobby_thread, args=())
    lobby.start()


def connect_lobby(connect_ip):
    """
    Creates a client SO which connects to an available server SO on the LAN via its IP address and port.

    Currently just accepts an IP address to connect to instead of looking for available IPs on the LAN.
    """

    try:
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_socket.connect((str(connect_ip), port))
        print("Connected to %s\n" % connect_ip)

    except ConnectionRefusedError:
        print("The Game doesn't exist!")

    '''
    print("Connecting to game server...")
    for IP in devices:
        try:
            conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn_socket.connect((IP, port))     # HALTS!
            if conn_socket.recv(1024) == b"response":
                break
            else:
                conn_socket.close()

        except ConnectionRefusedError:
            print("Removed ip ", IP)
            conn_socket.close()
            devices.remove(IP)

    if devices == []:
        print("No lobbies are currently open")
    else:
        print(devices)  # to test
        print("Connected to %s\n" % IP)
    '''


def close_lobby():
    """
    Creates a local "terminator" client SO which connects to the local server SO (if there is such) and signals closure.
    """

    term_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    term_client.connect((host, port))

'''
# Start the game

try:
    start_game(PLAYER_NAME, conn_socket, IS_SERVER)

finally:
    conn_socket.close()
'''