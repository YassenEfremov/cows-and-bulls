from tkinter import *

import cb_game_code.cb_lobby_controls as lobby_controls


if __name__ == "__main__":

    # Main window

    root = Tk()

    root.title("Cows and bulls")
    root.geometry("960x540")

    # Frames

    top = Frame(root, bg="blue")
    top.place(bordermode=OUTSIDE, relheight=0.2, relwidth=1.0)

    left = Frame(root, bg="green")
    left.place(bordermode=OUTSIDE, relheight=0.8, relwidth=0.5, rely=0.2, relx=0)

    right = Frame(root, bg="orange")
    right.place(bordermode=OUTSIDE, relheight=0.8, relwidth=0.5, rely=0.2, relx=0.5)

    # Lobby Buttons

    label_player_name = Label(top, text="Player Name")
    label_player_name.pack(side=TOP)

    player_name = Entry(top)
    player_name.pack(side=TOP)

    def start():
        lobby_controls.create_lobby()
        start_stop.configure(text="Cancel Game", command=stop)

    def stop():
        lobby_controls.close_lobby()
        start_stop.configure(text="Start Game", command=start)

    start_stop = Button(left, text="Start Game", command=start)
    start_stop.pack(side=TOP)

    conn_ip = Entry(right)
    conn_ip.pack(side=TOP)

    connect = Button(right, text="Connect to Game", command=lambda: lobby_controls.connect_lobby(conn_ip.get()))
    connect.pack(side=TOP)

    root.mainloop()
