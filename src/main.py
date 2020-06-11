from tkinter import *
import tkinter.font as tkFont
import threading
import queue

import cb_game_code.cb_lobby_controls as lobby_controls


if __name__ == "__main__":
    """
    This is the main file where all the widgets and other GUI components are drawn.
    """

    #                 #
    #   Main window   #
    #                 #

    root = Tk()

    root.title("Cows and bulls")
    root.geometry("960x540")
    root.minsize(820, 500)

    #           #
    #   Fonts   #
    #           #

    font_name = tkFont.Font(size=25)
    font_button = tkFont.Font(size=15)
    font_process = tkFont.Font(size=15, slant="italic")

    #            #
    #   Frames   #
    #            #

    top = Frame(root, bg="lightblue")
    top.place(relheight=0.2, relwidth=1.0)

    left = Frame(root, bg="green")
    left.place(relheight=0.8, relwidth=0.5, rely=0.2, relx=0)

    right = Frame(root, bg="orange")
    right.place(relheight=0.8, relwidth=0.5, rely=0.2, relx=0.5)

    #                              #
    #   Lobby Buttons and Labels   #
    #                              #

# Top Frame----------------------------------------------------------------------------------------------------------- #

    label_player_name = Label(top, text="Player Name", font=font_name)
    label_player_name.place(relx=0.5, rely=0.5, y=-25, anchor=CENTER)

    entry_player_name = Entry(top, width=10, font=font_name)
    entry_player_name.place(relx=0.5, rely=0.5, y=25, anchor=CENTER)

# Left Frame---------------------------------------------------------------------------------------------------------- #

    def start():
        label_waiting_game.place(relx=0.5, y=50, anchor=N)
        lobby_controls.create_lobby(entry_player_name.get())
        button_create_game.configure(text="Cancel Game", command=stop)

        if lobby_controls.create_lobby == "started":
            label_waiting_game.place_forget()
            label_player_name.place_forget()
            entry_player_name.place_forget()
            entry_conn_ip.place_forget()


    def stop():
        lobby_controls.close_lobby()
        label_waiting_game.place_forget()
        button_create_game.configure(text="Start Game", command=start)


    button_create_game = Button(left, text="Start Game", font=font_button, command=start)
    button_create_game.place(relx=0.5, y=10, anchor=N)

    label_waiting_game = Label(left, text="Waiting for opponent to join...", font=font_process, fg="gray")

# Right Frame--------------------------------------------------------------------------------------------------------- #

    def connect():
        # label_waiting_conn.place(relx=0.5, y=50, anchor=N)

        _state = queue.Queue()

        connection = threading.Thread(target=lobby_controls.connect_lobby_thread, args=[IP, _state])
        connection.start()

        if _state.get() == "invalid":
            label_invalid_game.place(relx=0.5, y=50, anchor=N)
            label_invalid_game.after(2000, label_invalid_game.place_forget)


    entry_conn_ip = Entry(right, width=14, font=font_button)
    entry_conn_ip.place(relx=0.5, y=10, x=-100, height=38, anchor=N)
    IP = entry_conn_ip.get()

    button_join_game = Button(right, text="Connect to Game", font=font_button, command=connect)
    button_join_game.place(relx=0.5, y=10, x=100, anchor=N)

    label_waiting_conn = Label(right, text="Connecting...", font=font_process, fg="gray")

    label_invalid_game = Label(right, text="The Game doesn't exist!", font=font_process, fg="gray")

    root.mainloop()
