from tkinter import *

import func_dir.lobby_controls as lobby_controls


if __name__ == "__main__":

    # Main window

    root = Tk()

    root.title("Cows and bulls")
    root.geometry("960x540")

    # Lobby Buttons

    def start():
        lobby_controls.create_lobby()
        start_stop.configure(text="Cancel Game", command=stop)

    def stop():
        lobby_controls.close_lobby()
        start_stop.configure(text="Start Game", command=start)

    start_stop = Button(root, text="Start Game", command=start)
    start_stop.pack(side=TOP)

    conn_ip = Entry(root)
    conn_ip.pack(side=TOP)

    connect = Button(root, text="Connect to Game", command=lambda: lobby_controls.connect_lobby(conn_ip.get()))
    connect.pack(side=TOP)

    root.mainloop()
