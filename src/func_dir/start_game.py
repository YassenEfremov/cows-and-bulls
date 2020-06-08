import getpass
import ast


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


def start_game(player_name, game_socket):
    print("Game begins!\n")

    # Take both players numbers

    my_number = input_number(player_name)

    # Initialize the player

    my_player = Player(player_name, my_number)

    # Take guesses

    is_my_turn = True

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
