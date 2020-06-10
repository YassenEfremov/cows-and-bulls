from tkinter import *
import tkinter.font as tkFont

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
    root.minsize(720, 480)

    #           #
    #   Fonts   #
    #           #

    name_font = tkFont.Font(size=20)

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

    # Top Frame------------------------------------------------------------------------------------------------------- #

    label_player_name = Label(top, text="Player Name", font=name_font)
    label_player_name.place(relx=0.5, rely=0.5, y=-25, anchor=CENTER)

    player_name = Entry(top, width=10, font=name_font)
    player_name.place(relx=0.5, rely=0.5, y=25, anchor=CENTER)

    # Left Frame------------------------------------------------------------------------------------------------------ #

    def start():
        lobby_controls.create_lobby()
        start_stop.configure(text="Cancel Game", command=stop)

    def stop():
        lobby_controls.close_lobby()
        start_stop.configure(text="Start Game", command=start)

    start_stop = Button(left, text="Start Game", command=start)
    start_stop.place(relx=0.5, y=10, anchor=N)

    # Right Frame----------------------------------------------------------------------------------------------------- #

    conn_ip = Entry(right, width=15)
    conn_ip.place(relx=0.5, y=10, x=-70, height=30, anchor=N)

    connect = Button(right, text="Connect to Game", command=lambda: lobby_controls.connect_lobby(conn_ip.get()))
    connect.place(relx=0.5, y=10, x=70, anchor=N)

    root.mainloop()
