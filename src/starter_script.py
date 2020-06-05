import socket
import getpass
import os
import sys
import getopt
import ast
import re
import random
from src.func_dir.get_lan_ips import *


class Player:

    def __init__(self, name, number_to_guess):
        self.name = name
        self._number_to_guess = number_to_guess
        print("Created player " + str(self))

    def guess(self, guess):
        bull = 0
        all_bulls_cows = 0  # total number of digit guessed perfectly. right place + wrong place

        num_as_str = str(self._number_to_guess)
        guess_as_str = str(guess)

        for i in range(0, 4):
            if num_as_str[i] == guess_as_str[i]:
                bull += 1
        for i in num_as_str:
            if i in guess_as_str:
                all_bulls_cows += 1

        cow = all_bulls_cows - bull

        return bull, cow


def input_number(player_name):  # Enter original number
    while True:
        try:
            num = int(getpass.getpass(player_name + "'s number: "))
            while len(str(num)) != 4:
                print("The number length is too short or too long, try again")
                num = int(getpass.getpass(player_name + "'s number: "))
            return num
        except ValueError:
            print("Type a number, not letters")


def make_a_guess(player_name):  # Enter a guess
    while True:
        try:
            guess = int(input(player_name + ", enter your guess: "))
            while len(str(guess)) != 4:
                print("The number length is too short or too long, try again")
                guess = int(input(player_name + ", enter your guess: "))
            return guess
        except ValueError:
            print("Type a number, not letters")


def start_game(player_name, game_socket, is_server):
    print("Game begins!\n")

    # Take both players numbers

    my_number = input_number(player_name)

    # Initialize the player

    my_player = Player(player_name, my_number)

    # Take guesses

    is_my_turn = is_server

    while True:
        if is_my_turn:
            guess = make_a_guess(player_name)
            game_socket.sendall(str(guess).encode("utf8"))
            guess_result = ast.literal_eval(str(game_socket.recv(1024).decode("utf8")))

            print("You have %s bulls and %s cows\n" % guess_result)
            have_winner = guess_result[0] == 4
            if have_winner:
                print("I won! Game Over!")
                return

            is_my_turn = not is_my_turn
        else:
            other_player_guess = int(game_socket.recv(1024).decode("utf8"))
            guess_result = my_player.guess(other_player_guess)

            game_socket.sendall(str(guess_result).encode("utf8"))

            print("other player has %s bulls and %s cows\n" % guess_result)
            have_winner = guess_result[0] == 4
            if have_winner:
                print("Other player won! Game Over!")
                return

            is_my_turn = not is_my_turn


if __name__ == "__main__":

    # Check parameters

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s", ["host=", "port=", "name="])
    except getopt.GetoptError:
        print(__file__ + " [-s] [--host HOST_NAME] [--port PORT_NUMBER] [--name PLAYER_NAME]")
        sys.exit(2)

    PLAYER_NAME = "Player" + str(random.randint(1, 100))
    IS_SERVER = False

    for opt, arg in opts:
        if opt == "-s":
            IS_SERVER = True
        if opt == "--host":
            host = arg
        if opt == "--port":
            port = int(arg)
        if opt == "--name":
            PLAYER_NAME = arg

    # Get host info + IPs

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
