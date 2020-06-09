from tkinter import *

import func_dir.lobby_controls as lobby_controls


if __name__ == "__main__":

    # Main window

    root = Tk()

    root.title("Cows and bulls")
    root.geometry("960x540")

    # Lobby Buttons

    start = Button(root, text="Start Game", command=lobby_controls.create_lobby)
    start.pack(side=TOP)

    stop = Button(root, text="Cancel", command=lobby_controls.close_lobby)
    stop.pack(side=TOP)

    conn_ip = Entry(root)
    conn_ip.pack(side=TOP)

    connect = Button(root, text="Connect to Game", command=lambda: lobby_controls.connect_lobby(conn_ip.get()))
    connect.pack(side=TOP)

    root.mainloop()
