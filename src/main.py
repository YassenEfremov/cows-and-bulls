import socket
import sys
import getopt
import random
from tkinter import *

from src.func_dir.get_lan_ips import *
from src.func_dir.start_game import *
from src.func_dir.lobby_controls import *


if __name__ == "__main__":

    # Check parameters
    '''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s", ["host=", "port=", "name="])

    except getopt.GetoptError:
        print(__file__ + " [-s] [--host HOST_NAME] [--port PORT_NUMBER] [--name PLAYER_NAME]")
        sys.exit(2)
    '''
    # Main window

    root = Tk()

    root.title("Cows and bulls")
    root.geometry("960x540")

    # Buttons

    start = Button(root, text="Start Game", command=create_lobby)
    start.pack(side=TOP)
    stop = Button(root, text="Cancel", command=close_lobby)
    stop.pack(side=TOP)

    root.mainloop()
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
'''
    host_name = socket.gethostname()  # Alone seen as localhost
    host = socket.gethostbyname(host_name + ".local")
    port = 5555

    devices = get_lan_ips()
    print(devices, host)

    # Create sockets

    print("Game process is server: %s;  Host: %s;  Port: %s" % (str(IS_SERVER), host, port))

    if IS_SERVER:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        print("Waiting for other opponent to join...")

        conn_socket, addr = server_socket.accept()
        print("Opponent connected from %s\n" % addr)

    else:
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to game server...")
        for IP in devices:
            try:
                conn_socket.connect((IP, port))

            except ConnectionRefusedError:
                devices.remove(IP)

        print(devices)
        print("Connected to %s\n" % IP)

    # Start the game

    try:
        start_game(PLAYER_NAME, conn_socket, IS_SERVER)

    finally:
        conn_socket.close()
'''