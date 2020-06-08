import socket
import random
import threading

from func_dir.get_lan_ips import *
from func_dir.start_game import *


# Check parameters
'''
try:
    opts, args = getopt.getopt(sys.argv[1:], "s", ["host=", "port=", "name="])

except getopt.GetoptError:
    print(__file__ + " [-s] [--host HOST_NAME] [--port PORT_NUMBER] [--name PLAYER_NAME]")
    sys.exit(2)
'''

PLAYER_NAME = "Player" + str(random.randint(1, 100))    # These will be changed in the future
IS_SERVER = True                                        #
'''
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
# Get host info + IPs

host_name = socket.gethostname()  # Alone seen as localhost
host = socket.gethostbyname(host_name + ".local")
port = 5555

devices = get_lan_ips()
print("local devices: ", devices, host)


# Main lobby functions

def create_lobby_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Waiting for other opponent to join...")

    conn_socket, addr = server_socket.accept()

    if addr[0] == host:
        print("Server closed")
        server_socket.close()
    else:
        print("Opponent connected from %s\n" % addr)
        start_game(PLAYER_NAME, conn_socket, IS_SERVER)


def create_lobby():
    lobby = threading.Thread(target=create_lobby_thread, args=())
    lobby.start()


def connect_lobby():
    conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to game server...")
    for IP in devices:
        try:
            conn_socket.connect((IP, port))

        except ConnectionRefusedError:
            devices.remove(IP)

    print(devices)
    print("Connected to %s\n" % IP)


def close_lobby():
    term_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    term_client.connect((host, port))
'''
# Start the game

try:
    start_game(PLAYER_NAME, conn_socket, IS_SERVER)

finally:
    conn_socket.close()
'''