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


def choose_number(player_name):  # Enter original number
    while True:
        try:
            number = int(input(player_name + "'s number: "))
            while len(str(number)) != 4:
                print("The number length is too short or too long, try again")
                number = int(input(player_name + "'s number: "))
            return number

        except ValueError:
            print("Type a number, not letters")


def take_a_guess(player_name):  # Enter a guess
    while True:
        try:
            guess = int(input(player_name + ", enter your guess: "))
            while len(str(guess)) != 4:
                print("The number length is too short or too long, try again")
                guess = int(input(player_name + ", enter your guess: "))
            return guess

        except ValueError:
            print("Type a number, not letters")


def start_game(player_name, game_socket, host):
    """
    This is where the whole game process begins.
    """

    print("Game begins!\n")

    # => TAKE BOTH PLAYERS NUMBERS <= #

    _num_sent = False
    _num_recv = False
    my_number = choose_number(player_name)

    # => INITIALIZE THE PLAYERS <= #

    my_player = Player(player_name, my_number)
    game_socket.sendall("valid".encode("utf8"))
    _num_sent = True

    _val_str = game_socket.recv(1024).decode("utf8")
    if _val_str == "valid":
        _num_recv = True

    if _num_sent and _num_recv:
        pass

    # => START GUESSING <= #

    #if host == "server":

    server_turn = True  # Will be changed to be more fair, e.g. a dice?

    while True:

        if server_turn:
            guess = take_a_guess(player_name)
            game_socket.sendall(str(guess).encode("utf8"))
            guess_result = ast.literal_eval(str(game_socket.recv(1024).decode("utf8")))

            print("You have %s bulls and %s cows\n" % guess_result)
            have_winner = guess_result[0] == 4

            if have_winner:
                print("I won! Game Over!")
                return

            server_turn = not server_turn

        else:
            opponent_guess = int(game_socket.recv(1024).decode("utf8"))
            guess_result = my_player.guess(opponent_guess)

            game_socket.sendall(str(guess_result).encode("utf8"))

            print("Other player has %s bulls and %s cows\n" % guess_result)
            have_winner = guess_result[0] == 4

            if have_winner:
                print("Other player won! Game Over!")
                return

            server_turn = not server_turn
